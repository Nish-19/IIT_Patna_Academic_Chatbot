from sklearn.externals import joblib 
def cgb(cat,sex,brh):
    # Load the model from the file
    model = joblib.load('models/cgb.pkl') 
    # Use the loaded model to make predictions 
    ge=0
    ob=0
    sc=0
    st=0
    m=0
    cs=0
    ce=0
    ee=0
    me=0
    if(cat=="ge" or cat=="general"):
        ge=1
    if(cat=="ob" or cat=="obc"):
        ob=1
    if(cat=="sc"or cat=="SC"):
        sc=1
    if(cat=="st"or cat=="ST"):
        st=1
    if(sex=="m"or sex=="M" or sex=="Male" or sex=="male"):
        m=1
    if(brh=="cs"):
        cs=1
    if(brh=="ce"):
        ce=1
    if(brh=="ee"):
        ee=1
    if(cat=="me"):
        me=1
    #input_array 
    inputs=[[ge,ob,sc,st,m,ce,cs,ee,me]]
    cpi=model.predict(inputs)
    if cpi[0] < 7.5:
        cpi[0]=cpi[0]+1

    return round(cpi[0],2)
#Please Convert cat,sex,brh etc to lowercase letters
cat=input("Enter the category:")
sex=input("Enter Gender:")
brh=input("Enter branch:")
print("Predicted CPI is:",cgb(cat,sex,brh))


def cpiPrediction(spi_1, spi_2):
    model2 = joblib.load('models/spi1_spi2_cpi.pkl') 
    inputs = [[spi_1, spi_2]]
    cpi = model2.predict(inputs)
    return round(cpi[0],2)

# spi_1 = float(input("Enter spi in sem 1:"))
# spi_2 = float(input("Enter spi in sem 2:"))
# print("Your Predicted CPI is: ",cpiPrediction(spi_1, spi_2) )

def ma102GradePrediction(grade1):
    model3 = joblib.load('models/ma101_ma102.pkl') 
    inputs = [[grade1]]
    grade2 = model3.predict(inputs)
    cp = grade2[0][0]
    return round(cp,0)
    
# grade = int(input("Enter grade in MA101:"))
# print("Your Predicted grade in MA102 is: ", ma102GradePrediction(grade))


