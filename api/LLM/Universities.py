_universities = """
University of Oxford	2
University of Cambridge	4
Imperial College London	6
University College London (UCL)	8
University of Edinburgh	15
The University of Manchester	28
Kings College London (KCL)	37
London School of Economics and Political Science (LSE)	56
University of Bristol	62
University of Warwick	64
University of Nottingham	94
University of Glasgow	98
University of Southampton	99
University of Birmingham	101
Queen Mary University of London	117
University of Leeds	121
University of Sheffield	124
University of Exeter	149
University of York	156
University of Liverpool	162
Newcastle University	164
Lancaster University	173
Durham University	187
University of Sussex	221
Other	999
"""

# This class is used to get the rank of a university based on its name from the _universities string above and return the rank as an integer

class University:
    def __init__(self):
        universities_list = _universities.strip().split("\n")
        self.universities_tuples = []

        for university in universities_list:
            # Split the line on the tab character
            university_name, rank = university.split("\t")
            # Convert the rank to an integer
            rank = int(rank)
            # Add the tuple to the list
            self.universities_tuples.append((university_name, rank))
        self.name_list = [university[0] for university in self.universities_tuples]
    # Get the rank of a university based on its name
    def get_rank(self, name):
        name = name.replace("'", "").replace("'", "").replace('"', "")
        for university in self.universities_tuples:
            if university[0].lower() == name.lower():
                return university[1]
        return None
# Get the list of university names as a list of strings
    def get_name_list(self):
        return self.name_list
# Get the list of university names and ranks as a list of tuples 
    def __str__(self):
        return f"{self.name} is ranked {self.rank}."
# Get the list of university names and ranks as a list of tuples 
    def __repr__(self):
        return f"University('{self.name}', {self.rank})"
