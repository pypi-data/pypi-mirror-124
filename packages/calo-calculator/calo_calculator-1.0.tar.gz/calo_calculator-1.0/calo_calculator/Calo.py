class Calo:
    """ Calo class for calculating daily calorie intake of a person
         based on his need.
        
        Attributes:
        genter (string) represnting the gender of a person (male or female)
        age (integer) representing the age of a person
        weight (float) represnting person's weight in kg
        height (float) represnting person's height in cm
    """
    
    def __init__(self, gender, age, weight, height):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        
        
    def calculate_bmr(self):
        """ Function to        
        
              
        Args: 
			none
		
		Returns: 
			float: BMR - Basal Metabolic Rate
        """
        mbr = 0
        if self.gender.lower() == "male":
            mbr = (self.weight * 10) + (self.height * 6.25) - (self.age * 5) + 5
        else:
            mbr = (self.weight * 10) + (self.height * 6.25) - (self.age * 5) - 161
        
        return mbr
    
    def calculate_total_calo(self, bmr, activ_level):
        """ Function to calculate person's total calories 
            based on his/her activity level
        
        Args: 
            bmr (float) representing person's daily BMR
			active_level (integer) represening person's active level (from 1 to 5)
		
		Returns: 
			float: calo - person's daily total calories
        """
        if activ_level == 1:
            return bmr * 1.2
        elif activ_level == 2:
            return bmr * 1.375
        elif activ_level == 3:
            return bmr * 1.55
        elif activ_level == 4:
            return bmr * 1.725
        elif activ_level == 5:
            return bmr * 1.9
        else:
            return 0
        
    def calculate_calo(self, active_level):
        
        """Function to calculate person's daily intake of food 
           based on Mifflin-St Jeor Equation
        
        Args: 
			active_level (integer) represening person's active level (from 1 to 4)
		
		Returns: 
			float: daily calories
        """
        self.gender = self.check_gender(self.gender)
        self.age = self.check_age(self.age)
        self.weight = self.check_weight(self.weight)
        self.height = self.check_height(self.height)
        
        bmr = self.calculate_bmr()
        calo = self.calculate_total_calo(bmr, self.check_active_level(active_level))
        
        return round(calo, 2)
                     
    def check_gender(self, gender):
        """ Function to check if the inserted gender is either male or female.
        
        Args:
            gender (string) represening person's gender
        
        Returns:
            string: person's gender
        """
        
        if gender.lower() == 'male' or gender.lower() == 'female':
            return gender.lower()
        else:
            print('Please enter correct gender type: male or female')
            exit() 
    
    def check_age(self, age):
        """ Function to check if the inserted age is integer.
        
        Args:
            age (integer) represening person's age
        
        Returns:
            string: person's age
        """
        
        if type(age) != int:
            print('Please enter correct age, integer')
            exit()
        if age < 10 or age > 100:
            print('Please enter correct age, range acceted (10-100)')
            exit()
            
        return age
    
    def check_weight(self, weight):
        """ Function to check if the inserted weight is a number.
        
        Args:
            weight (float) represening person's weight
        
        Returns:
            float: person's weight
        """
        
        if (type(weight) == int or type(weight) == float) and weight > 0:
            return weight
        else:
            print('Please enter correct weight')
            exit()
            
        
    
    def check_height(self, height):
        """ Function to check if the inserted height is a number.
        
        Args:
            height (float) represening person's height
        
        Returns:
            float: person's height
        """
        
        if (type(height) == int or type(height) == float) and height > 0:
            return height
        else:
            print('Please enter correct height')
            exit()
            
    def check_active_level(self, active_level):
        """ Function to check if the inserted active_level is integer.
        
        Args:
            active_level (integer) represening person's active_level
        
        Returns:
            integer: person's active_level
        """
        
        if type(active_level) != int:
            print('Please enter correct active level, integer')
            exit()
            
        return active_level
    