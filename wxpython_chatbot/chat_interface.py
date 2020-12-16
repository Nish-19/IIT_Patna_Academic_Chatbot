"""
Name: Nischal; Haindavi; Vaibhav; Garima; Souhardya
Roll: 1801CS33; 1801CS35; 1801CS58; 1801CS20; 1801CS51
Innovation Lab Project IIT-Patna
Interface for running the main chatbot code
"""


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
        self.rbox = wx.RadioBox(self.panel, label = 'Type', choices = ['DB', 'Non-DB'], majorDimension=1, style = wx.RA_SPECIFY_ROWS) 
        self.rbox.SetSelection(0)
        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        # trying to insert image
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
        self.feedback_file = open('feedback.csv', 'a+')
        self.embedding_matrix, self.tokenizer, self.MAX_LENGTH, self.db, self.nlp = initialize()
        string = "Thanks for your patience!\nI am ready! Let\'s Start!"
        self.result.SetLabel(string)

    def OnButton(self, e):
        utter = self.editname.GetValue()
        if utter == "quit":
        	get_sentiment_report(self.sentiment_polarity)
        	self.feedback_file.close()
        	sys.exit(0)
        else:
	        choice, output = get_output(utter, self.embedding_matrix, self.tokenizer, self.MAX_LENGTH, self.db, self.nlp)
	        output = str(output)
	        print(output)
	        if choice == 0:
	        	self.rbox.SetSelection(1)
	        elif choice == 1:
	        	self.rbox.SetSelection(0)
	        if output == "None":
	            string = "Not working as expected\nFeedback recorded!\nPlease check the most similar sounding queries\n"
	            similar_queries = find_similarity(utter)
	            print(similar_queries)
	            for query in similar_queries:
	            	print(query)
	            	string+=query + "\n"
	            self.result.SetValue(string)         
	            string = utter + "," + str(choice) + "\n"
	            self.feedback_file.write(string)
	            # Opening the feedback module
	        else:
	        	self.result.SetValue(output)
	        self.sentiment_polarity.append(get_polarity(utter))

    def onRadioBox(self, e):
    	pass

app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()