#BİLGİSAYARDA PROGRAMLAMA DERSİ PROJESİ 
#Emre Yapıcı - 222080533@ogr.uludag.edu.tr    GİTHUB: emreyapici16
#Furkan Özkan -222080516@ogr.uludag.edu.tr    GİTHUB: furkanozkan16
#Elif Acun -   222180541@ogr.uludag.edu.tr    GİTHUB: elifacun

#Opencv kütüphanesi kullanılara çeşitli el hareketlerini algılayıp ve algılanan bu hareketi anlamlandırarak anlamlı bir sonuç çıkartılıyor projemizde



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
