# Web_Crawler_V2

## Not: Hiçbir sorumluluk kabul etmiyorum
![Ekran Resmi 2020-03-23 13 08 10](https://user-images.githubusercontent.com/25556230/77305626-6e3e5980-6d07-11ea-910e-d42d2bfd199e.png)

## Kullanım
```
python dereliUrlv2.py -u https://example.com -o output.txt
```

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
