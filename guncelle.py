import json
import requests

# GitHub bilgilerin
GITHUB_TOKEN = "github_pat_xxxxxxxxxxxx"  # ⬅️ GitHub token'ını yapıştır
REPO = "kullaniciadi/depo"                # ⬅️ Kullanıcı adın/depo adın
FILE_PATH = "fiyatlar.json"               # ⬅️ Dosya adı

# GitHub API ile dosyayı güncelle
def github_update(data):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    
    # Önce dosyanın SHA'sını al (güncellemek için gerekli)
    response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json()["sha"]
    
    # Yeni veriyi gönder
    payload = {
        "message": "Menü güncellendi",
        "content": json.dumps(data).encode('utf-8').hex(),
        "sha": sha,
        "branch": "main"
    }
    
    response = requests.put(url, json=payload, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    print("✅ Güncellendi!" if response.ok else f"❌ Hata: {response.text}")

# Kullanıcıdan input al
def menu_yonet():
    menu = []
    
    while True:
        print("\n📋 MENÜ YÖNETİMİ")
        print("1. Yeni ürün ekle")
        print("2. Ürün sil")
        print("3. Fiyat güncelle")
        print("4. Menüyü göster")
        print("5. Kaydet ve çık")
        
        secim = input("Seçim: ")
        
        if secim == "1":
            id = len(menu) + 1
            name = input("Ürün adı: ")
            desc = input("Açıklama: ")
            category = input("Kategori (yemek/sicak-icecek/soguk-icecek/tatli): ")
            icon = input("Emoji (🍔): ")
            badge = input("Etiket (POPÜLER/YENİ/ACILI): ")
            badgeType = input("Etiket rengi (popular/new/spicy/hot/cold/dessert): ")
            price = float(input("Fiyat: "))
            
            menu.append({
                "id": id,
                "name": name,
                "desc": desc,
                "category": category,
                "icon": icon,
                "badge": badge,
                "badgeType": badgeType,
                "price": price
            })
            print(f"✅ {name} eklendi!")
            
        elif secim == "2":
            for i, item in enumerate(menu):
                print(f"{i+1}. {item['name']}")
            sil = int(input("Silmek istediğin ürün numarası: ")) - 1
            silinen = menu.pop(sil)
            print(f"🗑️ {silinen['name']} silindi!")
            
        elif secim == "3":
            for i, item in enumerate(menu):
                print(f"{i+1}. {item['name']} - {item['price']} TL")
            no = int(input("Fiyatı değiştirilecek ürün numarası: ")) - 1
            yeni_fiyat = float(input("Yeni fiyat: "))
            menu[no]["price"] = yeni_fiyat
            print(f"✅ Fiyat güncellendi!")
            
        elif secim == "4":
            for item in menu:
                print(f"{item['icon']} {item['name']} - {item['price']} TL")
                
        elif secim == "5":
            data = {"menu": menu}
            github_update(data)
            print("✅ GitHub'a kaydedildi!")
            break

menu_yonet()
