# Web_Crawler_V2

## Kullanım
python dereliUrlv2.py -u https://example.com -o output.txt

## Program akışı
+ Verilen siteye istek yapar.
+ İstek yollanan sitenin kaynak kodlarındaki bütün URL'leri alır.
+ Daha fazla URL ulaşmak için google modülü ile 50 tane daha URL alıyoruz.
+ Bu toplanan URL'leri şu şekilde ayırma işlemine geçiriyoruz.
```
      https.//example.com/test/test1/test2
      |
      |_______test1
      |_________test1/test2
      |____________test1/test2/test3
      |_______________test1/test2/test3/test4 
```
+ Elde edilen dizinlere tekrar istek yaparak yeni URL'ler elde ediyoruz.

## Geliştirilecek
+ Bütün URL'lere Payloadlar deneme özelliğini eklemeyi planlıyorum. Bu sayede otamatik güvenlik açığı tarama özelliği gelmiş olucak.
+ URL alma özellikleri geliştirilecek
