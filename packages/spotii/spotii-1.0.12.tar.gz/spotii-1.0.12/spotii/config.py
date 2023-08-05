import time
import json
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import main_paras

if sys.platform == 'linux':
    PROFILE_FOLDER = '/home/pi/app/spotii'
else:
    PROFILE_FOLDER = currentdir


#defaultLanguage = 'English'

DEFAULT_LANGUAGE = 'English'


basic = {
    'language': DEFAULT_LANGUAGE,
    'time_zone':''
    }


class Config():
    def __init__(self):
        print('working folder', PROFILE_FOLDER)
        self.languageList = os.listdir(os.path.join(currentdir, main_paras.defaultLanguageFolder))        
        self.profile_list = {
            'basic': basic,
            'person': [],
            }
        if time.daylight:
            offsetHour = time.altzone / 3600
        else:
            offsetHour = time.timezone / 3600
        self.profile_list['basic']['time_zone'] = 'Etc/GMT%+d' % offsetHour        

        try:
            with open(os.path.join(PROFILE_FOLDER,'profile.json'), 'r') as infile:
                self.profile_list = json.load(infile)
                if self.profile_list['basic']['language'] not in self.languageList:
                    self.profile_list['basic']['language'] = DEFAULT_LANGUAGE
        except Exception as e:
            print(e)

        print ('init Before: ', time.strftime('%X %x %Z'))
        os.environ['TZ'] = self.profile_list['basic']['time_zone']
        if sys.platform == 'linux':
            time.tzset()
        print ('init After: ', time.strftime('%X %x %Z'))
            
        
    def save(self):
        with open(os.path.join(PROFILE_FOLDER,'profile.json'), 'w+') as fp:
            json.dump(self.profile_list, fp, sort_keys=True, indent=4)
    def setCurrentLanguage(self,index):
        self.profile_list['basic']['language']=self.languageList[index]
        self.save()

    def getLanguageList(self):
        return self.languageList

    def getCurrentLanguage(self):
        return self.profile_list['basic']['language']

    def setDefaultTimeZone(self):
        if time.daylight:
            offsetHour = time.altzone / 3600
        else:
            offsetHour = time.timezone / 3600
        self.profile_list['basic']['time_zone'] = 'Etc/GMT%+d' % offsetHour        
        self.save()
        
    def setTimeZone(self, timeZone):
        self.profile_list['basic']['time_zone']=timeZone
        print ('Before: ', time.strftime('%X %x %Z'))
        os.environ['TZ'] = timeZone
        if sys.platform == 'linux':
            time.tzset()
        print ('After: ', time.strftime('%X %x %Z'))
        self.save()

    def getTimeZone(self):
        return self.profile_list['basic']['time_zone']
        
    def getProfile(self, user):
        profile = main_paras.empty.copy()
        for person in self.profile_list['person']:
            if user == person['user']:
                for key in profile:
                    if key in person.keys():
                        profile[key] = person[key]
                break;
        return profile
    def setProfile(self, profile):
        for i, person in enumerate(self.profile_list['person']):
            if profile['user'] == person['user']:
                self.profile_list['person'][i] = profile
                break;
        else:
            self.profile_list['person'].append(profile)        
        self.save()

    def clear(self):
        self.profile_list = {
            'basic': basic,
            'person': [],
            }
        self.save()

    def show(self):
        print(self.profile_list)
        
        
   



##    print(profile)
##    with open('profile.json', 'w') as fp:
##        json.dump(profile, fp, sort_keys=True, indent=4)
##    
##    with open('profile.json', 'r') as infile:
##        data = json.load(infile)
##    print('from file',data)
##          


    
if __name__ == "__main__":
    pass              
