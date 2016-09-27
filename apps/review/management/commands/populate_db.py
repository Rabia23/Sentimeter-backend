__author__ = 'rabia'
from apps.area.models import Area
from apps.region.models import Region
from apps.city.models import City
from apps.branch.models import Branch
from django.contrib.auth.models import User
from apps.person.models import UserInfo
from apps.question.models import Question
from apps.option.models import Option
from apps.promotion.models import Promotion
from apps.questionnaire.models import Questionnaire
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def create_patches(self):
        patches_list = [{"area": {"name": "North"}, "region": {"name": "Khurram"}, "city": {"name": "Lahore"},
                        "branch": {"name": "Gulberg", "benchmark_count": 200, "longitude": 73.071891, "latitude": 33.585263}}]

        for patch in patches_list:
            area = Area.objects.create(name=patch['area']['name'])
            region = Region.objects.create(name=patch['region']['name'], area=area)
            city = City.objects.create(name=patch['city']['name'], region=region)
            branch = Branch.objects.create(name=patch['branch']['name'], city=city,
                                           benchmark_count=patch['branch']['benchmark_count'],
                                           longitude=patch['branch']['longitude'],
                                           latitude=patch['branch']['latitude'])

            self.stdout.write("Area "+area.name+" successfully created.")
            self.stdout.write("Region "+region.name+" successfully created.")
            self.stdout.write("City "+city.name+" successfully created.")
            self.stdout.write("Branch "+branch.name+" successfully created.")

    def create_management(self):
        management_list = [{"user": {"first_name": "Director", "last_name": "Sentimeter", "username": "sentimeter.director",
                                     "password": "arbisoft", "email": "danial.zahid@arbisoft.com"},
                            "userinfo": {"phone_no": "11111111111", "role": 7}}]
        #Add management
        director = User.objects.create_user(first_name="Director", last_name="Sentimeter", username="sentimeter.director",
                                       password="arbisoft", email="danial.zahid@arbisoft.com",)
        director_info = UserInfo.objects.create(phone_no="11111111111", role=7, user=director)
        self.stdout.write("Director "+director.username+" successfully created.")

        assistant_director = User.objects.create_user(first_name="Assistant", last_name="Director", username="assistant.director",
                                                 password="arbisoft", email="aamish.baloch@gmail.com")
        assistant_director_info = UserInfo.objects.create(phone_no="11111111111", role=6, user=assistant_director,
                                                          parent=director_info)
        self.stdout.write("Assistant Director "+assistant_director.username+" successfully created.")

        operational_manager = User.objects.create_user(first_name="Operational", last_name="Manager",
                                                  username="operation.manager", password="arbisoft", email="danial.zahid@arbisoft.com")
        operational_manager_info = UserInfo.objects.create(phone_no="11111111111", role=5, user=operational_manager,
                                                           parent=assistant_director_info)
        self.stdout.write("Operational Manager "+operational_manager.username+" successfully created.")

        operational_region = Region.objects.get(name="Khurram")
        operational_consultant = User.objects.create_user(first_name="Operational", last_name="Consultant",
                                                     username="operation.consultant", password="arbisoft", email="danial.zahid@arbisoft.com")
        operational_consultant_info = UserInfo.objects.create(phone_no="11111111111", region=operational_region, role=4,
                                                              user=operational_consultant, parent=operational_manager_info)
        self.stdout.write("Operational Consultant "+operational_consultant.username+" successfully created.")

        branch = Branch.objects.get(name="Gulberg")
        branch_manager = User.objects.create_user(first_name="Branch", last_name="Manager", username="branch.manager",
                                             password="arbisoft", email="branch.manager@gmail.com")

        branch_manager_info = UserInfo.objects.create(phone_no="11111111111", branch=branch, role=3, user=branch_manager,
                                                      parent=operational_consultant_info)
        self.stdout.write("Branch Manager "+branch_manager.username+" successfully created.")

        branch_gro = User.objects.create_user(first_name="adnan", last_name="zahid", username="adnan.zahid",
                                         password="arbisoft", email="adnan@gmail.com")
        branch_gro_info = UserInfo.objects.create(phone_no="11111111111", branch=branch, role=2, user=branch_gro,
                                                  parent=branch_manager_info)
        self.stdout.write("Branch Gro "+branch_gro.username+" successfully created.")

    def create_questions_options(self):
        questions_list = [
                          {
                            "question": {
                              "text": "How can we provide you a better experience?",
                              "text_urdu": "ہم آپ کو بہتر سہولیات کیسے فراہم کر سکتے ہیں؟",
                              "type": 2,
                              "genreType": 0
                            },
                            "options": [
                              {
                                "text": "Cleanliness",
                                "text_urdu": "صفائی",
                                "color_code": "#1f9aec",
                                "suboptions": [
                                  {
                                    "text": "Employees",
                                    "text_urdu": "ملازمین",
                                    "color_code": "#4CCC72"
                                  },
                                  {
                                    "text": "Lobby",
                                    "text_urdu": "ماحول",
                                    "color_code": "#3598DC"
                                  },
                                  {
                                    "text": "Rest Rooms",
                                    "text_urdu": "بیت الخلا",
                                    "color_code": "#9C59B8"
                                  },
                                  {
                                    "text": "Lobby Temperature",
                                    "text_urdu": "لابی کا درجہ حرارت",
                                    "color_code": "#34495E"
                                  },
                                  {
                                    "text": "Music",
                                    "text_urdu": "موسیقی",
                                    "color_code": "#F0C547"
                                  },
                                  {
                                    "text": "Table/Chairs",
                                    "text_urdu": "میز / کرسیاں",
                                    "color_code": "#E74D3D"
                                  },
                                  {
                                    "text": "Floor",
                                    "text_urdu": "فرش",
                                    "color_code": "#ff9900"
                                  },
                                  {
                                    "text": "Car Parking",
                                    "text_urdu": "کار پارکنگ",
                                    "color_code": "#aa6600"
                                  }
                                ]
                              },
                              {
                                "text": "Quality",
                                "text_urdu": "معیار",
                                "color_code": "#cb1e24",
                                "suboptions": [
                                  {
                                    "text": "Not Fresh",
                                    "text_urdu": "باسی کھانا",
                                    "color_code": "#4CCC72"
                                  },
                                  {
                                    "text": "Taste",
                                    "text_urdu": "ذائقہ",
                                    "color_code": "#3598DC"
                                  },
                                  {
                                    "text": "Fries",
                                    "text_urdu": "چپس",
                                    "color_code": "#9C59B8"
                                  }
                                ]
                              },
                              {
                                "text": "Service",
                                "text_urdu": "خدمت",
                                "color_code": "#ffd200",
                                "suboptions": [
                                  {
                                    "text": "Employee Attentiveness",
                                    "text_urdu": "ملازمین کی توجہ",
                                    "color_code": "#4CCC72"
                                  },
                                  {
                                    "text": "Speed of Service",
                                    "text_urdu": "سروس کی رفتار",
                                    "color_code": "#3598DC"
                                  },
                                  {
                                    "text": "Wrong Order",
                                    "text_urdu": "غلط آرڈر",
                                    "color_code": "#9C59B8"
                                  },
                                  {
                                    "text": "Missing Order",
                                    "text_urdu": "نامکمّل آرڈر",
                                    "color_code": "#34495E"
                                  },
                                  {
                                    "text": "Employee Courtesy",
                                    "text_urdu": "عملی شائستگی",
                                    "color_code": "#F0C547"
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "question": {
                              "text": "How was your experience today?",
                              "text_urdu": "آپ کا تجربہ آج کیسا رہا؟",
                              "type": 1,
                              "genreType": 0
                            },
                            "options": [
                              {
                                "text": "I'm lovin' it",
                                "text_urdu": "بہترین",
                                "color_code": "#0E590A"
                              },
                              {
                                "text": "Everything on track",
                                "text_urdu": "ٹھیک",
                                "color_code": "#01ad0f"
                              },
                              {
                                "text": "Few concerns",
                                "text_urdu": "چند مسائل",
                                "color_code": "#e73a3a"
                              },
                              {
                                "text": "Not happy enough",
                                "text_urdu": "برا",
                                "color_code": "#ac1a1a"
                              }
                            ]
                          },
                          {
                            "question": {
                              "text": "What would make you visit McDonald's more often?",
                              "text_urdu": "آپ زیادہ کثرت سے مکدونلڈس کس لئے آئیں گے؟",
                              "type": 3,
                              "genreType": 0
                            },
                            "options": [
                              {
                                "text": "Quality of Food",
                                "text_urdu": "کھانے کا معیار",
                                "color_code": "#4CCC72"
                              },
                              {
                                "text": "Friendly & Courteous Staff",
                                "text_urdu": "دوستانہ اور شائستہ عملہ",
                                "color_code": "#3598DC"
                              },
                              {
                                "text": "Clean Restaurant",
                                "text_urdu": "صاف ریستوران",
                                "color_code": "#E74D3D"
                              },
                              {
                                "text": "Variety in Menu",
                                "text_urdu": "متنوع مینو",
                                "color_code": "#F0C547"
                              },
                              {
                                "text": "Special Promotions",
                                "text_urdu": "خاص پروموشنز",
                                "color_code": "#9C59B8"
                              }
                            ]
                          },
                          {
                            "question": {
                              "text": "How likely are you to recommend this Restaurant to your friends or family?",
                              "text_urdu": "آپکے اپنے دوستوں یا خاندان کو اس ریستوران کا مشورہ دینے کے کتنے امکانات ہیں؟",
                              "type": 20,
                              "genreType": 0
                            },
                            "options": [
                              {
                                "text": "1",
                                "text_urdu": "1",
                                "color_code": "#ac1a1a"
                              },
                              {
                                "text": "2",
                                "text_urdu": "2",
                                "color_code": "#ac1a1a"
                              },
                              {
                                "text": "3",
                                "text_urdu": "3",
                                "color_code": "#e73a3a"
                              },
                              {
                                "text": "4",
                                "text_urdu": "4",
                                "color_code": "#e73a3a"
                              },
                              {
                                "text": "5",
                                "text_urdu": "5",
                                "color_code": "#e73a3a"
                              },
                              {
                                "text": "6",
                                "text_urdu": "6",
                                "color_code": "#01ad0f"
                              },
                              {
                                "text": "7",
                                "text_urdu": "7",
                                "color_code": "#01ad0f"
                              },
                              {
                                "text": "8",
                                "text_urdu": "8",
                                "color_code": "#01ad0f"
                              },
                              {
                                "text": "9",
                                "text_urdu": "9",
                                "color_code": "#0E590A"
                              },
                              {
                                "text": "10",
                                "text_urdu": "10",
                                "color_code": "#0E590A"
                              }
                            ]
                          }
                        ]
        for ques in questions_list:
            question = Question.objects.create(text=ques['question']['text'], text_urdu=ques['question']['text_urdu'],
                                               type=ques['question']['type'], genreType=ques['question']['genreType'])
            self.stdout.write(question.text+" successfully created.")
            for op in ques['options']:
                option = Option.objects.create(text=op['text'], text_urdu=op['text_urdu'], question=question, color_code=op['color_code'])
                self.stdout.write(option.text+" successfully created.")
                if 'suboptions' in op:
                    for sub_op in op['suboptions']:
                        sub_option = Option.objects.create(text=sub_op['text'], text_urdu=sub_op['text_urdu'], parent=option, color_code=sub_op['color_code'])
                        self.stdout.write(sub_option.text+" successfully created.")

    def create_promotion(self):
        promotion_list = [
                          {
                            "promotion": {
                              "title": "Waffle Cone"
                            },
                            "questions": [
                              {
                                "text": "How did you come to know about the promotion?",
                                "type": 5,
                                "genreType": 1,
                                "text_urdu": "آپ کو پروموشن کے بارے میں کیسے پتا چلا؟",
                                "options": [
                                  {
                                    "text": "Print",
                                    "text_urdu": "",
                                    "color_code": "#E74D3D"
                                  },
                                  {
                                    "text": "Radio",
                                    "text_urdu": "",
                                    "color_code": "#F0C547"
                                  },
                                  {
                                    "text": "Digital",
                                    "text_urdu": "",
                                    "color_code": "#34495E"
                                  },
                                  {
                                    "text": "Billboards",
                                    "text_urdu": "",
                                    "color_code": "#9C59B8"
                                  },
                                  {
                                    "text": "Restaurants",
                                    "text_urdu": "",
                                    "color_code": "#3598DC"
                                  },
                                  {
                                    "text": "Fliers",
                                    "text_urdu": "",
                                    "color_code": "#4CCC72"
                                  }
                                ]
                              },
                              {
                                "text": "Is it a good value for money?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "یہ پیسے کے لئے ایک اچھی قیمت ہے؟",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "ہاں",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              },
                              {
                                "text": "Are you satisfied with the taste?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "کیا آپ ذائقے سے مطمئن ہیں؟",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              },
                              {
                                "text": "Are you satisfied with the product?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "آپ اس مصنوع سے مطمئن ہیں؟",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              }
                            ]
                          }
                        ]

        for promo in promotion_list:
            promotion = Promotion.objects.create(title=promo['promotion']['title'])
            self.stdout.write(promotion.title+" successfully created.")
            for ques in promo['questions']:
                question = Question.objects.create(text=ques['text'], type=ques['type'], genreType=ques['genreType'], text_urdu=ques['text_urdu'], promotion=promotion)
                self.stdout.write(question.text+" successfully created.")
                for op in ques['options']:
                    option = Option.objects.create(text=op['text'], text_urdu=op['text_urdu'], question=question, color_code=op['color_code'])
                    self.stdout.write(option.text+" successfully created.")

    def update_promotion(self, promotion_id):
        promotion_list = [
                          {
                            "promotion": {
                              "title": "Beef Range"
                            },
                            "questions": [
                              {
                                "text": "Which burger did you have?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": ' ',
                                "options": [
                                  {
                                    "text": "Spicy Jalapeño",
                                    "text_urdu": ' ',
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "Mushroom Melt",
                                    "text_urdu": ' ',
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              },
                              {
                                "text": "How did you come to know about the promotion?",
                                "type": 5,
                                "genreType": 1,
                                "text_urdu": "آپ کو پروموشن کے بارے میں کیسے پتا چلا؟",
                                "options": [
                                  {
                                    "text": "Radio",
                                    "text_urdu": "",
                                    "color_code": "#E74D3D"
                                  },
                                  {
                                    "text": "Fliers",
                                    "text_urdu": "",
                                    "color_code": "#F0C547"
                                  },
                                  {
                                    "text": "Billboards",
                                    "text_urdu": "",
                                    "color_code": "#34495E"
                                  },
                                  {
                                    "text": "Restaurants",
                                    "text_urdu": "",
                                    "color_code": "#9C59B8"
                                  },
                                  {
                                    "text": "Internet/ Social Media",
                                    "text_urdu": "",
                                    "color_code": "#3598DC"
                                  },
                                  {
                                    "text": "Newspapers/ Magazines",
                                    "text_urdu": "",
                                    "color_code": "#4CCC72"
                                  }
                                ]
                              },
                              {
                                "text": "Is it a good value for money?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "یہ پیسے کے لئے ایک اچھی قیمت ہے؟",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "ہاں",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  },
                                  {
                                    "text": "Not Sure",
                                    "text_urdu": " ",
                                    "color_code": "#4CCC72"
                                  }
                                ]
                              },
                              {
                                "text": "Are you satisfied with the taste?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "کیا آپ ذائقے سے مطمئن ہیں؟",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  },
                                  {
                                    "text": "Not Sure",
                                    "text_urdu": " ",
                                    "color_code": "#4CCC72"
                                  }
                                ]
                              },
                              {
                                "text": "Are you satisfied with the product?",
                                "type": 4,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "آپ اس مصنوع سے مطمئن ہیں؟",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  },
                                  {
                                    "text": "Not Sure",
                                    "text_urdu": " ",
                                    "color_code": "#4CCC72"
                                  }
                                ]
                              }
                            ]
                          }
                        ]

        for promo in promotion_list:
            promotion = Promotion.objects.get(pk=promotion_id)
            self.stdout.write(promotion.title)
            for ques in promo['questions']:
                question = Question.objects.create(text=ques['text'], type=ques['type'], genreType=ques['genreType'], text_urdu=ques['text_urdu'], promotion=promotion)
                self.stdout.write(question.text+" successfully created.")
                for op in ques['options']:
                    option = Option.objects.create(text=op['text'], text_urdu=op['text_urdu'], question=question, color_code=op['color_code'])
                    self.stdout.write(option.text+" successfully created.")

    def create_questionnaire(self, branch_id):
        questionnaire_list = [
                          {
                            "questionnaire": {
                              "title": "Jail Road"
                            },
                            "questions": [
                              {
                                "text": "How often do you visit McDonald's?",
                                "type": 11,
                                "genreType": 1,
                                "text_urdu": "آپ مکڈونلڈ کتنی بار آتے ہیں؟",
                                "options": [
                                  {
                                    "text": "Daily",
                                    "text_urdu": "",
                                    "color_code": "#E74D3D"
                                  },
                                  {
                                    "text": "Monthly",
                                    "text_urdu": "",
                                    "color_code": "#F0C547"
                                  },
                                  {
                                    "text": "Weekly",
                                    "text_urdu": "",
                                    "color_code": "#34495E"
                                  },
                                  {
                                    "text": "Very Rare",
                                    "text_urdu": "",
                                    "color_code": "#9C59B8"
                                  }
                                ]
                              },
                              {
                                "text": "Which city are you from? (If not from Lahore)",
                                "type": 11,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Dina",
                                    "text_urdu": "",
                                    "color_code": "#4CCC72"
                                  },
                                  {
                                    "text": "Kharian",
                                    "text_urdu": "",
                                    "color_code": "#90ec7c"
                                  },
                                  {
                                    "text": "Mirpur",
                                    "text_urdu": "",
                                    "color_code": "#f1d400"
                                  },
                                  {
                                    "text": "Kotli",
                                    "text_urdu": "",
                                    "color_code": "#434347"
                                  },
                                  {
                                    "text": "Gujrat",
                                    "text_urdu": "",
                                    "color_code": "#178aea"
                                  },
                                  {
                                    "text": "Other",
                                    "text_urdu": "",
                                    "color_code": "#cb1e24"
                                  }
                                ]
                              },
                              {
                                "text": "Through what medium have you come to know of this branch?",
                                "type": 11,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Print",
                                    "text_urdu": "",
                                    "color_code": "#4CCC72"
                                  },
                                  {
                                    "text": "Friend/Family",
                                    "text_urdu": "",
                                    "color_code": "#90ec7c"
                                  },
                                  {
                                    "text": "Digital",
                                    "text_urdu": "",
                                    "color_code": "#f1d400"
                                  },
                                  {
                                    "text": "Billboards",
                                    "text_urdu": "",
                                    "color_code": "#434347"
                                  },
                                  {
                                    "text": "Restaurants",
                                    "text_urdu": "",
                                    "color_code": "#178aea"
                                  },
                                  {
                                    "text": "Fliers",
                                    "text_urdu": "",
                                    "color_code": "#cb1e24"
                                  }
                                ]
                              },
                              {
                                "text": "Did you know before traveling that there is a McDonald's Branch Jail Road?",
                                "type": 12,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "ہاں",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              },
                              {
                                "text": "In which direction are you traveling?",
                                "type": 12,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "RWP/ISD to Lahore",
                                    "text_urdu": "",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "Lahore to RWP/ISD",
                                    "text_urdu": "",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              },
                              {
                                "text": "Are you from Lahore?",
                                "type": 12,
                                "genreType": 1,
                                "text_urdu": "",
                                "options": [
                                  {
                                    "text": "Yes",
                                    "text_urdu": "ہاں",
                                    "color_code": "#f7ca17"
                                  },
                                  {
                                    "text": "No",
                                    "text_urdu": "نہیں",
                                    "color_code": "#e84c3d"
                                  }
                                ]
                              }
                            ]
                          }
                        ]

        for questionnaire in questionnaire_list:
            q = Questionnaire.objects.create(title=questionnaire['questionnaire']['title'])
            branch = Branch.objects.get(pk=branch_id)
            q.branch.add(branch)
            self.stdout.write(q.title+" successfully created.")
            for ques in questionnaire['questions']:
                question = Question.objects.create(text=ques['text'], type=ques['type'], genreType=ques['genreType'], text_urdu=ques['text_urdu'], questionnaire=q)
                self.stdout.write(question.text+" successfully created.")
                for op in ques['options']:
                    option = Option.objects.create(text=op['text'], text_urdu=op['text_urdu'], question=question, color_code=op['color_code'])
                    self.stdout.write(option.text+" successfully created.")

    def add_arguments(self, parser):
        parser.add_argument(
            '-branch_id',
            type=int,
            dest='branch_id',
            help='Add branch Questionnaire',
        )
        parser.add_argument(
            '-promotion_id',
            type=int,
            dest='promotion_id',
            help='Update Promotion',
        )

    def handle(self, *args, **options):
        if options['branch_id']:
            branch = options['branch_id']
            print("branch id: ", branch)
            # self.create_questionnaire(branch)

        if options['promotion_id']:
            promotion_id = options['promotion_id']
            print("promotion id: ", promotion_id)
            self.update_promotion(promotion_id)

        # self.create_patches()
        # self.create_management()
        # self.create_questions_options()
        # self.create_promotion()