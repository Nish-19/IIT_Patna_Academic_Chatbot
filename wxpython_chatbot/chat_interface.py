"""
Name: Nischal A
Roll: 1801CS33
Innovation Lab Project IIT-Patna
Interface for running the main chatbot code
"""


#from chatbot_new import *
from chatbot_new import *
from sentence_similarity_new import *
import wx, sys

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        self.panel = wx.Panel(self)
        self.heading = wx.StaticText(self.panel, label="IIT Patna Academic Alexa", style=wx.ALIGN_CENTRE)
        self.heading.SetFont(wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        self.heading.SetForegroundColour(wx.RED)     
        self.quote = wx.StaticText(self.panel, label="Chatbot:")
        #self.result = wx.StaticText(self.panel, label="")
        self.result = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH, size=(540, 200))
        self.result.SetForegroundColour(wx.BLUE)
        self.button = wx.Button(self.panel, label="Enter")
        self.lblname = wx.StaticText(self.panel, label="Your Question:")
        self.editname = wx.TextCtrl(self.panel, size=(540, -1))
        self.rbox = wx.RadioBox(self.panel, label = 'Type', choices = ['Non-DB', 'DB'], majorDimension=1, style = wx.RA_SPECIFY_ROWS) 
        self.rbox.SetSelection(0)
        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        # insert a picture of 100*100 size of your choice
        bmp = wx.Bitmap('iitp_resize.png') 
        self.imgbutton = wx.Button(self.panel, label="", size = (100,100))
        self.imgbutton.SetBitmap(bmp) 

        # self.jpg1 = wx.Image('nischal_resize.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # self.imgbutton = wx.StaticBitmap(self, -1, self.jpg1, (10 + self.jpg1.GetWidth(), 5), (self.jpg1.GetWidth(), self.jpg1.GetHeight()))

        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(30, 30)
        self.sizer.Add(self.imgbutton, (0,0))
        self.sizer.Add(self.heading, (0,1))
        self.sizer.Add(self.lblname, (1, 0))
        self.sizer.Add(self.editname, (1, 1))
        self.sizer.Add(self.quote, (2, 0))
        self.sizer.Add(self.result, (2, 1))
        self.sizer.Add(self.rbox, (3,0))
        self.sizer.Add(self.button, (4, 0), (3, 2))

        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)  
        self.SetSizerAndFit(self.windowSizer)  

        # Set event handlers
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

        # Trying to call initialize
        string = "Hello! My name is academic chatbot. I am here at your service\nPlease wait! I am configuring myself"
        self.result.SetLabel(string)
        self.sentiment_polarity = []
        self.embedding_matrix, self.tokenizer, self.MAX_LENGTH, self.db, self.nlp = initialize()
        string = "Thanks for your patience!\nI am ready! Let\'s Start!"
        self.result.SetLabel(string)

        # Feedback initialization
        self.type_input = 0
        self.class_feedback_file = open('class_feedback.csv', 'a+')
        self.db_feedback_file = open('db_feedback_file.csv', 'a+')
        self.ndb_feedback_file = open('ndb_feedback_file.csv', 'a+')
        self.prev_string = ''
        self.prev_selection = -1

    def OnButton(self, e):
        utter = self.editname.GetValue()
        if utter == "quit":
            get_sentiment_report(self.sentiment_polarity)
            self.class_feedback_file.close()
            self.db_feedback_file.close()
            self.ndb_feedback_file.close()
            sys.exit(0)
        else:
            if self.type_input == 0:
    	        choice, output = get_output(utter, self.embedding_matrix, self.tokenizer, self.MAX_LENGTH, self.db, self.nlp)
    	        output = str(output)
    	        print(output)
    	        if choice == 0:
    	        	self.rbox.SetSelection(0)
    	        elif choice == 1:
    	        	self.rbox.SetSelection(1)
    	        if output == "None":
                    string = "Not working as expected\nChose appropriate type button and press next to record the feedback!\n"
                    # similar_queries = find_similarity(utter)
                    # print(similar_queries)
                    # for query in similar_queries:
                    # 	print(query)
                    # 	string+=query + "\n"
                    self.result.SetValue(string)         
                    # string = utter + "," + str(choice) + "\n"
                    # self.feedback_file.write(string)
                    # Opening the feedback module
                    self.type_input = 1
                    self.prev_string = utter
                    self.prev_selection = self.rbox.GetSelection()
    	        else:
    	        	self.result.SetValue(output)
    	        self.sentiment_polarity.append(get_polarity(utter))
            elif self.type_input == 1:
                # Running the feedback module here
                new_choice = self.rbox.GetSelection()
                if new_choice != self.prev_selection:
                    string = self.prev_string + "," + str(new_choice) + "\n"
                    self.class_feedback_file.write(string)
                elif new_choice == self.prev_selection and new_choice == 1:
                    self.db_feedback_file.write(self.prev_string + "\n")
                elif new_choice == self.prev_selection and new_choice == 0:
                    self.ndb_feedback_file.write(self.prev_string + "\n")
                string = "Thank You for the feedback! Please also look at similar sounding queries\n"
                similar_queries = find_similarity(self.prev_string)
                print(similar_queries)
                for query in similar_queries:
                  print(query)
                  string+=query + "\n"
                string+="You may now enter your next question\n"
                self.result.SetValue(string)
                self.type_input = 0 


    def onRadioBox(self, e):
    	pass

app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()