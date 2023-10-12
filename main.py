import cv2
from cvzone.HandTrackingModule import HandDetector
class button:

      def __init__(self,pos,width,height,value):
        self.pos=pos
        self.height=height
        self.value=value
        self.width=width
      def draw(self,img):
          cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
          cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50),
                        3)
          cv2.putText(img,self.value, (self.pos[0]+20,self.pos[1]+50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
      def clickcheck(self,x,y):

          if (self.pos[0]<x<self.pos[0]+self.width) and (self.pos[1]<y<self.pos[1]+self.height) :
              cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                            cv2.FILLED)
              cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50),
                            3)
              cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN, 3,
                          (50, 50, 50), 2)

              return True
          else:
              return False


cap =cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
buttonvalue=[['7','8','9','*'],
             ['4','5','6','-'],
             ['1','2','3','+'],
             ['0','/','.','=']]
buttonlist=[]

for x in range(4):
    for y in range(4):
       xpos = x*70+600
       ypos = y*70+ 200
       buttonlist.append(button((xpos,ypos),70,70,buttonvalue[y][x]))
myeq=''
dc=0
result=''
detect=HandDetector(detectionCon=0.8,maxHands=1)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hand,imge = detect.findHands(img)
    cv2.rectangle(img,(600,100),(880,200),(280,280,280),cv2.FILLED)
    cv2.rectangle(img, (600, 100), (880, 200), (50, 50, 50), 3)
    for button in buttonlist:
        button.draw(img)
# processing
    #check for hands
    if hand :
        lmList=hand[0]['lmList']
        length,info, imgs = detect.findDistance(lmList[8],lmList[12],img) #distance between middle and index finger
        x,y,z=lmList[8]
        if length<50:
          for i, button in enumerate(buttonlist):
            if (button.clickcheck(x,y)) and (dc == 0):
                value=buttonvalue[int(i%4)][int(i/4)]
                if value == "=":
                    result=str(eval(myeq))
                    myeq=''
                else:
                    myeq += value
                dc=1#delaycounter


    if dc != 0:
      dc+=1
      if dc > 10:
         dc=0

    
#display results
    cv2.putText(img,myeq,(610,140),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)
    cv2.putText(img, result, (815, 180), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    cv2.imshow('ftg',imge)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()