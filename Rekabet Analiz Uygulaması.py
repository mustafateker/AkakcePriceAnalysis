import requests
from bs4 import BeautifulSoup
import locale
import pandas as pd
import time

# Dosya ile import yapınız!
# Rekabet Analizi Programı
# Akakçe sitesinden girilen url'lerdeki ürünlerin en uygun 
# fiyatlı ürünün satıcı ve fiyat bilgisini çekerek pandas
# kütüphanesini de kullanarak excel tablosuna aktaran kod

# Kod sadece Akakçe ürün listesi sayfasında çalışmaktadır. Soup classları otomatik tanıyamadığı için etiket ve class kontrollerini
# Akakçe sitesi için manuel yapmak durumunda kaldım
#       Gerekli yüklemeler  : 
#  (terminal)     pip install openpyxl
#  (terminal)     pip install pandas
#  (terminal)     pip install bs4

def get_price_analysis(url):
    # User-Agent belirliyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Soup kütüphanesi için html içeriğini ayrıştırıyoruz
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ürün adını soup objesine atıyoruz
        product_title_tag = soup.find('h1')
        if product_title_tag:
            product_title = product_title_tag.get_text().strip()
            print(f"Ürün adı bulundu: {product_title}")
        else:
            print("Ürün adı bulunamadı.")
            return []

        # Satıcı ve fiyat bilgilerini çekiyoruz
        sellers_list = soup.find_all('li', class_='c')
        product_data = []

        if sellers_list:
            # Sadece en uygun satıcının adı ve fiyatını çekiyoruz
            for seller in sellers_list:
                price_tag = seller.find('span', class_='pt_v8')
                seller_info = seller.find('span', class_='v_v8')

                if seller_info:
                    seller_info_img = seller_info.find('img')
                    if seller_info_img:
                        seller_info_img_alt = seller_info_img['alt']
                    else:
                        seller_info_img_alt = "Image not found"
                        seller_info_text = seller_info.get_text(strip=True)

                    if price_tag:
                        # Fiyat lokalizasyonunu yapıyoruz
                        locale.setlocale(locale.LC_NUMERIC, "tr_TR.UTF-8")
                        price = locale.atof(price_tag.get_text().strip().replace(' TL', ''))
                        
                        print(f"Satıcı bulundu: {seller_info_img_alt}/{seller_info_text}, Fiyat: {price}")
                        
                        # Verileri sözlüğe ekliyoruz
                        product_data.append({
                            'Product Title': product_title,
                            'Seller': f"{seller_info_img_alt}/{seller_info_text}",
                            'Price': price
                        })
        else:
            print("Satıcı listesi bulunamadı.")
            return []

        return product_data

    else:
        print(f"HTTP isteği başarısız oldu, durum kodu: {response.status_code}")
        return []

# Ürün URL listesi
urls = [
    'https://www.akakce.com/laptop-notebook/en-ucuz-lenovo-v15-g4-amn-82yu0122tx-ryzen-5-7520u-8-gb-256-gb-ssd-radeon-610m-15-6-full-hd-notebook-fiyati,610308936.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-lenovo-v15-g3-82tt008ptx-i5-1235u-16-gb-512-gb-ssd-iris-xe-graphics-15-6-full-hd-notebook-fiyati,413793386.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-dell-vostro-3510-n8004vn3510emea01-u-i5-1135g7-8-gb-256-gb-15-6-ubuntu-fhd-dizustu-bilgisayar-fiyati,1445233889.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vs-2000-2d-masaustu-fiyati,1714275622.html',
    'https://www.akakce.com/bilgisayar-kasasi/en-ucuz-msi-mpg-sekira-100r-fanli-e-atx-oyuncu-kasasi-fiyati,889390357.html',
    'https://www.akakce.com/oyun-bilgisayari/en-ucuz-hp-victus-15-fa1042nt-7p8m3ea-i5-13500h-8-gb-512-gb-ssd-rtx4050-15-6-full-hd-notebook-fiyati,315471925.html',
    'https://www.akakce.com/akilli-saat/en-ucuz-general-mobile-gm-buddy-pembe-akilli-cocuk-saati-fiyati,119616961.html',
    'https://www.akakce.com/akilli-saat/en-ucuz-general-mobile-gm-buddy-akilli-cocuk-saati-fiyati,494595845.html',
    'https://www.akakce.com/cep-telefonu/en-ucuz-realme-note-50-128-gb-mavi-fiyati,641846672.html',
    'https://www.akakce.com/cep-telefonu/en-ucuz-realme-note-50-128-gb-siyah-fiyati,641846673.html',
    'https://www.akakce.com/ssd/en-ucuz-samsung-1-tb-980-mz-v8v1t0bw-m-2-pci-express-3-0-fiyati,1071263472.html',
    'https://www.akakce.com/switch/en-ucuz-zyxel-gs-105b-5-port-gigabit-10-100-1000-fiyati,974805538.html',
    'https://www.akakce.com/ssd/en-ucuz-kioxia-500-gb-exceria-lrc10z500gg8-m-2-pci-express-3-0-fiyati,706880562.html',
    'https://www.akakce.com/ssd/en-ucuz-intenso-512-gb-top-3812450-2-5-sata-3-0-fiyati,1033779155.html',
    'https://www.akakce.com/ssd/en-ucuz-western-digital-green-sn350-wds100t3g0c-1-tb-3200-2500-mb-s-m-2-nvme-fiyati,1956488359.html',
    'https://www.akakce.com/ram/en-ucuz-netac-basic-ntb-8gb-3200mhz-ddr4-ntbsd4n32sp-08-fiyati,1208311847.html',
    'https://www.akakce.com/ram/en-ucuz-netac-basic-ddr4-3200-8gb-u-dimm-ntbsd4p32sp-08-fiyati,1153433324.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-dell-vostro-3520-n1614pvnb3520u-i3-1215u-8-gb-256-gb-ssd-uhd-graphics-15-6-full-hd-notebook-fiyati,618722701.html',
    'https://www.akakce.com/oyun-bilgisayari/en-ucuz-hp-victus-15-fa1042nt-7p8m3ea-i5-13500h-8-gb-512-gb-ssd-rtx4050-15-6-full-hd-notebook-fiyati,315471925.html',
    'https://www.akakce.com/ssd/en-ucuz-hikvision-256-gb-hs-desires-256g-2-5-sata-3-0-fiyati,61731062.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-hp-250-g10-8a540ea-i5-1340p-16-gb-512-gb-ssd-iris-xe-graphics-15-6-full-hd-notebook-fiyati,384786092.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-hp-250-g8-854f4es-i5-1135g7-8-gb-256-gb-ssd-iris-xe-graphics-15-6-full-hd-notebook-fiyati,340286854.html',
    'https://www.akakce.com/harddisk/en-ucuz-seagate-3-5-1-tb-skyhawk-st1000vx005-sata-3-0-5900-rpm-hard-disk-fiyati,17290322.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-zetronic-zsw-232-karekod-ve-fiyati,548886289.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-zetronic-zsw-231-kablosuz-fiyati,548886288.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-zetronic-zs-223-kablolu-lazer-113-fiyati,1767803848.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-zetronic-zs-260-masaustu-karekod-ve-fiyati,2109056523.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-zetronic-zs-226-2d-karekod-fiyati,912640940.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-asus-vivobook-m1603qa-mb511-ryzen-5-5600h-8-gb-512-gb-radeon-graphics-16-wuxga-notebook-fiyati,384488045.html',
    'https://www.akakce.com/laptop-notebook/en-ucuz-hp-250-g8-853u8es-i5-1135g7-8-gb-256-gb-ssd-iris-xe-graphics-15-6-full-hd-notebook-fiyati,182059007.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vs-2000-2d-masaustu-fiyati,1714275622.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vsw-122-2d-fiyati,815334487.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vsk-118-2d-fiyati,815334485.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vsk-117-1d-fiyati,815334484.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vs-113-1d-fiyati,828726788.html',
    'https://www.akakce.com/barkod-okuyucu/en-ucuz-tiwox-vs-111-fiyati,815334482.html',
    'https://www.akakce.com/ssd/en-ucuz-msi-spatium-m390-nvme-m-2-1tb-nvme-m-2-1tb-r3300-w3000-fiyati,1635755066.html',
    'https://www.akakce.com/anakart/en-ucuz-msi-pro-h610m-b-intel-lga1700-ddr4-micro-atx-fiyati,1799769989.html',
    'https://www.akakce.com/direksiyon-seti/en-ucuz-kontorland-ft-096-fiyati,737407.html'
]

all_product_data = []

for url in urls:
    print(f"URL işleniyor: {url}")
    product_data = get_price_analysis(url)
    if product_data:
        all_product_data.extend(product_data)
    time.sleep(2)  # Sunucunun aşırı yüklenmesini engellemek için 2 saniye delay ekliyoruz

# Ürünleri DataFrame'e çeviriyoruz ve Excel dosyası ile dışa aktarıyoruz
if all_product_data:
    df = pd.DataFrame(all_product_data)
    df.to_excel('akakce_price_analysis.xlsx', index=False)
    print("Veriler Excel dosyasına kaydedildi: akakce_price_analysis.xlsx")
else:
    print("Herhangi bir veri bulunamadı.")