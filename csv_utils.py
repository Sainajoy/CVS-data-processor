import csv
import ipdb
import random
import datetime

from types import MethodType
from typing import Union, Iterable
from pathlib import Path
from model import TrainingData, KnownSample, InvalidSampleError, TrainingKnownSample, TestingKnownSample

from data_keys import species_key, sepal_length_key, sepal_width_key, petal_length_key, petal_width_key

def load( self, raw_data_iter: Iterable[dict[str, str]], data_size: int,
          testing_percentage: float=0.20, seed=None, is_verbose: bool=True ) -> int:
    """
    Extract TestingKnownSample and TrainingKnownSample from raw data
    Reads data dictionaries, splits them randomly into testing/training sets, filters out invalid samples, and returns the count of corrupted rows
    """
    #set the random seed if one is provided
    if seed is not None:
        random.seed(seed)

    #figure out the testing split
    testing_size = int(data_size * testing_percentage)
    data_indices = set(range(data_size)) #gets the data indices
    testing_indices = set(random.sample(list(data_indices), k=testing_size)) #randomly selects indices of k size for testing

    corrupted_count = 0

    for index, row in enumerate(raw_data_iter): #iteration and unpacking
        try:
            #sort the data into testing or training
            #classes from model.py help us build the objects

            if index in testing_indices:
                sample = TestingKnownSample.from_dict(row)  #.from_dict() method automatically validates the data and init parameters
                self.testing.append(sample) #self.testing is in TrainingData class
            else:
                sample = TrainingKnownSample.from_dict(row)
                self.training.append(sample)

        except:
            corrupted_count += 1
            
            # we add 1 to match the assignment's expected output format.
            if is_verbose:
                print(f"### WARNING: Row {index + 1}: Invalid species in {row}")
    return corrupted_count 
# Monkey-patch load() onto the TrainingData class
#
TrainingData.load = load








def read( self, data_filepath: Union[str, Path], testing_percentage=.20,
          seed=None, is_verbose=True, **kwargs ) -> (list[dict], int):
    """
     Reads a CSV file into a list of dictionaries, uses load() to create training/testing sets, and returns the data 
    and corrupted count
    """
 #convert the filepath to a Path object. It eases extraction of file name later
    filepath = Path(data_filepath)
    raw_data = [] #will be a list of dictionaries

    #Open the file and read it using DictReader
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # convert the reader object(which is a dictionary) into a list of dictionaries
        raw_data = list(reader)

    #call load() method which populates self.testing and self.training
    #self means the current TrainingData object we are working with not just any other global function 
    corrupted_count = self.load(raw_data_iter = raw_data, data_size = len(raw_data), is_verbose=is_verbose)

    if is_verbose:

        training_count = len(self.training)
        testing_count = len(self.testing)
        total = training_count + testing_count

        #filepath.name extracts just the filename and extension from the full path
        print(f"--- Read data from {filepath.name} (total={total}, training={training_count}, testing={testing_count})")

    return raw_data, corrupted_count
    
TrainingData.read = read
    



def to_dict( self, is_include_classification: bool=False ) -> dict:

    output_dict = {
        species_key : self.species,
        sepal_length_key : self.sepal_length,
        sepal_width_key : self.sepal_width,
        petal_length_key : self.petal_length,
        petal_width_key : self.petal_width,
    }

    if is_include_classification:
        output_dict['classification']: getattr(self, 'classification', None)

    return output_dict
        
KnownSample.to_dict = to_dict # Monkey-patching to_dict()






def from_dict( cls, row: dict[str, str] ) -> "KnownSample":
    """
    """
    #checks if the species is spelled correctly
    if row["species"] not in {"Iris-setosa", "Iris-versicolour", "Iris-virginica"}:
        raise InvalidSampleError(f"invalid species in {row!r}")
    try:
     #converts the strings to floats and passes them to the standard__init__method(cls)
        return cls (
            species = row[species_key],
            sepal_length=float(row[sepal_length_key]),
            sepal_width=float(row[sepal_width_key]),
            petal_length=float(row[petal_length_key]),
            petal_width=float(row[petal_width_key])
        )
        
    except ValueError as ex:
        raise InvalidSampleError(f"invalid {row!r}")    
    
KnownSample.from_dict = MethodType( from_dict, KnownSample ) # Monkey-patching a class method!







def save( self, data_filepath: Union[str, Path], is_overwrite: bool=False, 
          is_include_classification: bool=False, is_force=False, is_verbose: bool=True ) -> None:
    """
    """
    filename = Path(data_filepath)

    if filename.exists():
        if not is_overwrite:
            raise FileExistsError(f"Overwrite mode is OFF. Will not overwrite existing file '{filename.name}'!")
        elif is_overwrite:
            if is_verbose:
                print(f"The output file '{filename.name}' already exists and is being written over")

    all_dictionaries = []

    #sample - Objects (KnownSamples)
    for sample in self.training + self.testing:
        #KnownSample.to_dict() method takes on the same-named parameter, is_include_classification.
        output_dict = sample.to_dict(is_include_classification = is_include_classification)
        all_dictionaries.append(output_dict)
        
    if all_dictionaries:
        with open(filename, mode='w', newline = '', encoding='utf-8') as file:
            header_names = all_dictionaries[0].keys()
            writer = csv.DictWriter(file, fieldnames = header_names)
            
            writer.writeheader()
            writer.writerows(all_dictionaries)

TrainingData.save = save