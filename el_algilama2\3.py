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
