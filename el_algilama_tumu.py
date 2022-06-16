#BİLGİSAYARDA PROGRAMLAMA DERSİ PROJESİ 
#Emre Yapıcı - 222080533@ogr.uludag.edu.tr    GİTHUB: emreyapici16
#Furkan Özkan -222080516@ogr.uludag.edu.tr    GİTHUB: furkanozkan16
#Elif Acun -   222180541@ogr.uludag.edu.tr    GİTHUB: elifacun

#Opencv kütüphanesi kullanılara çeşitli el hareketlerini algılayıp ve algılanan bu hareketi anlamlandırarak anlamlı bir sonuç çıkartılıyor projemizde

#projenin 1/3 lük bölümüdür emre yapıcıya aittir

#Opencv fonksiyonlarını kullanabilmek için opencv kütüphanesini dahil ediyoruz
import cv2

#Morfolojik işlemler oluşturmak numpy kütüphanesini kullanacağız numpy kütüphanesini dahil ediyoruz
import numpy as np

#Yapılacak olan matematiksel işlemler için matematik kütüphanesini dahil ediyoruz
import math

#Opencv'nin VideoCapture fonksiyonu ile görüntüyü webcam veya dahili kameradan alıp vid değişkeninin içinde tutuyoruz
#Eğer birden fazla kamera varsa VideoCapture fonksiyonunun parantez içindeki değer 0'dan başlayarak artarak devam eder kameralar arası geçiş yapılabilir
#Anlık görüntü yerine hazır bir video kullanılacaksa parantez içine videonun adresi (pathi) belirtilir
vid = cv2.VideoCapture(0)
     
#Yapılan işlemleri sonsuza kadar çalıştırmak için while (1)-(true) döngüsü oluşturuyoruz
while(1):

#try except bloğu kullanılarak herhangi bir şey tespit edilmese bile program hata vermeyip devam edecektir
    try:  
        #Yakalanan videodaki kareleri tek tek okumak için vid.read fonksiyonu kullanılır 
        #read fonksiyonu 2 değer döndürür ilki video doğru okunduysa true doğru okunmadıysa false değerini döndürür, ikincisi de frame yani karelerdir 
        ret, frame = vid.read()

        #kameradan gelen görüntü bize ters şekilde gözükmektedir flip fonksiyonu ile gelen görüntüyü y eksenine göre tersine çeviriyoruz 
        #flip fonksiyonunun içinde çevirilecek değişken ve sayılar vardır. 1 yazarak y eksenine göre tersini almış olduk 
        frame=cv2.flip(frame,1)
        
        #morfolojik işlemlerde kullanmak için kernel tanımlaması yapıyoruz
        # 3e 3 lük 1'lerden oluşan bir matris oluşturuyoruz daha sonra bu matrisi görüntünün üzerine getirerek görüntüde bozdurma işlemi uygulanacaktır
        kernel = np.ones((3,3),np.uint8)
        
        #kamera açıldığında görüntünün x'te ve y'de 100'e 300 alanını işaretleyerek elimizi o alana götürerek el hareketleri o alanda algılanacaktır
        roi=frame[100:300, 100:300]
        
        #roi ile belirlenen alanı frame üzerinde bir dikdörtgen içine alacağız
        #renkler BGR biçiminde tanımlı olduğundan (0,255,0) değeri bize yeşil renginde dikdörtgen oluşturacaktır en sondaki sıfır değeri ise çizginin kalınlığıdır
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    

        #belli bir alandaki rengi diğer renklerden ayırmak için o bölgenin renk modunu BGR'den HSV moduna çevirmemiz gerekecek
        #maskeleme işlemi yaparken HSV modunu kullanmak bizim için kolaylık sağlayacağı için bu moda çeviriyoruz
        #sadece roideki seçili olan alan hsv moduna dönüştürülecektir
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        #elimizin diğer renklerden ayırabilmemiz için elimizin renk aralığını belirlememiz gerekir deri rengimiz için 1 alt ve 1 üst değer belirteceğiz
        # yapılan denemeler sonucunda elimizin renk aralığı alt değerde (0,20,70) üst değerde (20,255,255) olarak bulunmuştur
        # farklı insanların deri rengine göre bu aralığın değiştirilmesi gerekebilir 
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
        #roi alanında olan elimizi kalan alandan ayırıyoruz
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        #ayırma işleminden sonra oluşabilecek karanlık noktaları beyaz noktalarla dolduracağız
        #mask üzerinde 3e 3lük 1'lerden oluşan kernel ile siyah noktaları beyazlaştıracağız ve bu işlemin iterations ile 4 kere uygulanması gerektiğini belirtiyoruz
        mask = cv2.dilate(mask,kernel,iterations = 4)
        
        #görüntü üzerinde oluşan gürültüler için blurlama işlemi yapacağız
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
        #blurlama işleminde azalan gürültüden sonra konturları(sınır çizgileri) bulmak için findContours fonksiyonunu kullanıyoruz
        _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #konturların max alanını belirlemek için max fonksiyonunu kullanıyoruz
        #max fonksiyonu giriş olarak aldığı değerlerden en büyüğünü çıktı olarak döndürüyor
        #giriş olarak contours'u girersek bize en büyük kontur değerini döndürecektir
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
        #kontura biraz daha yakınlaşarak sınır çizgilerinin daha iyi çizilmesini sağlamak için daha önce deneyerek bulunmuş olan bir değer ile arcLength(kontur çevresini hesaplar)
        #çarparak epsilon değeri elde edilir 
        #approxPolyDP ile belirtilen hassasiyetle eğri veya çokgeni daha az köşesi olan başka eğri veya çokgen ile yaklaştırarak aralarında belirtilen mesafeye eşit olmasını sağlar
        #bu yapıya Douglas-Peucker algoritması denir
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        #elimizin çevresini dışbükey bir örtü oluşturarak oluşturulan örtünün kordinatlarını hull değişkeninin içinde saklıyoruz
        hull = cv2.convexHull(cnt)
        
        #hull değişkeninin içindeki kordinatları kullanarak o kordinatlarda oluşacak şeklin alanı ve elimizin alanı hesaplanıyor 
        areaHull = cv2.contourArea(hull)
        areaCnt = cv2.contourArea(cnt)
      
        #hull değişkeninde elimizin olmadığı örtülü alanın yüzde kaç olduğu hesaplanıyor
        areaRatio=((areaHull-areaCnt)/areaCnt)*100
    
        #dışbükey kusurlar tespit ediliyor bu kusurlar ele bağlı olan kusurlardır 
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
        #projenin 2/3 lük bölümüdür furkan özkana aittir
        
        #toplam kusur sayısına sıfır veriliyor
        l=0
        
        #defects içindeki kusurların değerlerini tek tek değişkenlere atılıyor daha sonrasında o değişkenler çizimde kullanılacaktır
        #örneğin defects'in değeri 15 ise i'yi 0'dan 15'e kadar dolaştıracaktır
        for i in range(defects.shape[0]):
            #s,e,f,d başlangıç bitiş,uzaklık değerlerini alıyor 
            s,e,f,d = defects[i,0]

            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            
            #start,end,far kordinatlarını birbirinden çıkartıp karesini alarak daha sonra karekökünü alıp elimizde oluşan üçgenin kenarının uzunluğunu buluyoruz 
            #elimizle iki yaptığımızda oluşan iki adet kenar ile  kenarların uzunluğuna erişebiliyoruz 
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            #oluşan üçgenin alanını bulmak için üçgenin tüm kenar uzunlukları toplanır ve ikiye bölünür daha sonra
            #oluşan s değerinden tüm uzunlukları çıkartıp çarpıyoruz ve tekrardan bu değeri s ile çarpıp karekökünü alıyoruz ve üçgenin alanını buluyoruz
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            #noktalar ve dışbükey arasında oluşan mesafeyi buluyoruz
            d=(2*ar)/a
            
            #iki kenar arasındaki açıya ulaşmak için kosinüs teoremi uygulanır
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
            #oluşan açı değeri 90'a eşit veya küçükse ve d 30dan büyükse kusur sayısını 1 arttırıyoruz
            if angle <= 90 and d>30:
                l += 1
                #roi bölgesindeki far olan(en uzak noktalara) 3 yarıçaplı mavi renkte içi dolu daire çiziyoruz 
                cv2.circle(roi, far, 3, [255,0,0], -1)
            
            #başlangıç ve bitiş noktaları kullanılarak roi üzerinde kalınlığı 2 olan yeşil renkte çizgi çiziyoruz
            cv2.line(roi,start, end, [0,255,0], 2)
            
        #kusuru tekrar 1 arttırıyoruz    
        l+=1
        
        #kusurlara bağlı tespitler yapılacaktır ilk olarak yazı fontunu belirliyoruz
        font = cv2.FONT_HERSHEY_SIMPLEX
        #eğer kusur 1'e eşitse
        if l==1:
            #eğer areacnt değeri 2000'den küçükse(bu değer deneme yanılmayla bulunmuştur)
            if areaCnt<2000:
                #ğer bu şartlar sağlanıyorsa yani elimizi kutunun içinde algılayamadıysa Elinizi Kutunun Icine Getirin yazacaktır
                cv2.putText(frame,'Elinizi Kutunun Icine Getirin',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            else:
                #elimizin olmadığı alanın yüzdesi 12den küçükse (bu değerler deneme yanılmayla bulunmuştur)
                if areaRatio<12:
                    #elimiz kutunun içinde ve elimizle bir şey yapmıyorsak ekranda 0 yazacaktır
                    cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                    #projenin3/3 lük bölümüdür elif acuna aittir
                    
                #elimizin olmadığı alan 17.5tan küçükse    
                elif areaRatio<17.5:
                    cv2.putText(frame,'best luck',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                   
                else:
                    #1 kusur var ve elimizin olmadığı alanın yüzdesi 17.5'ten büyükse elimizin 1 yaptığını algılar
                    cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        #eğer kusur sayısı 2 ise tespit eder ve ekranda 2 yazar            
        elif l==2:
            cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==3: #eğer kusur sayısı 3 ise 

              #eğer elimizin olmadığı alanın yüzdesi 27den küçükse elimizi 3 olarak algılar ve ekrana 3 yazar  
              if areaRatio<27:
                    cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              #eğer 27den büyükse ekrana ok yazar
              else:
                    cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
        #kusur sayısı 4 ise elimizi 4 olarak algılar ve ekrana 4 yazar            
        elif l==4:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
        #kusur sayısı 5 ise elimizi 5 olarak algılar ve ekrana 4 yazar    
        elif l==5:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
        #kusur sayısı 6 ise elimizin tanımlanan değerlerin dışında olur ve yeniden elimizi konumlandırmamızı ister ve ekrana reposition yazar    
        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        #yapılan maskeleme  işlemini mask penceresinde gösteriyoruz    
        cv2.imshow('mask',mask)
        #frame ekranımızı frame isimli pencerede gösteriyoruz
        cv2.imshow('frame',frame)
    except:
        pass
        
    #esc tuşuna basılırsa çalışmayı kapatacaktır
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

 #tüm pencereler kapatılır   
cv2.destroyAllWindows()
#görüntüyü okuduğumuz vid değişkeni serbest bırakılır
vid.release()    
    
