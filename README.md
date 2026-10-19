# FLEX AND FIT (Python + Flask)

This starter shop is configured for a fashion catalogue with clothes, shoes, bags and accessories. It supports product search/category filters, product detail pages, sizes, WhatsApp order links, and a simple password-protected product manager.

## Run on Windows

1. Install Python from https://www.python.org/downloads/
2. Extract the ZIP file and open Command Prompt in the `fashion_shop` folder.
3. Run:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   set SHOP_NAME=FLEX AND FIT
   set WHATSAPP_NUMBER=254780572505 and WHATSAPP_NUMBER_2=254798230681
   set ADMIN_PASSWORD=choose-a-strong-password
   set SECRET_KEY=use-a-long-random-secret
   python app.py
   ```
4. Open http://127.0.0.1:5000
5. Go to http://127.0.0.1:5000/admin to manage products.

Replace `2547XXXXXXXX` with your WhatsApp number in international digits-only format. Keep passwords and secret keys private.

## Publish for a shareable link

The localhost address works only on your computer. To share a public link, deploy this project to a Python-capable host. Set `SHOP_NAME`, `WHATSAPP_NUMBER`, `ADMIN_PASSWORD`, and `SECRET_KEY` as environment variables in the host dashboard. Use `gunicorn app:app` as the start command if requested. The host will provide the public URL.

## Payments and storage

This starter provides a product catalogue and WhatsApp ordering; it does not yet take or verify M-Pesa payments or provide a full cart/checkout. You selected M-Pesa and cash on delivery, so payment instructions can be added next. Do not ask customers to send PINs or passwords. Product data is stored in `products.json`; configure persistent storage on the host, otherwise some platforms may reset it during restarts or redeployments. Before taking real orders, test security and hosting persistence.
