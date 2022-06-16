#projenin 3\3lük kısmıdır elif acuna aittir

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
    
