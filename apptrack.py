from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'a0365944c4029819074695803944e2f2b05f0c17f10fa575eab73911fd885b83:'  # Clé secrète pour les sessions

# Fonction pour formater les montants en nombres flottants
def format_amount(amount):
    if isinstance(amount, str):
        amount = amount.replace('€', '').replace(' ', '').strip()
        amount = amount.replace(',', '.')
        if amount.endswith('.'):
            amount = amount[:-1]
        return float(amount)
    return float(amount)

# Fonction pour formater les montants en chaîne de caractères (format monétaire)
def format_amount_str(amount):
    return f"{amount:,.2f} €".replace(',', ' ').replace('.', ',').replace(' ', '.')

# Route pour la page d'accueil
@app.route('/')
def index():
    # Initialiser les données de commande dans la session
    session['order_data'] = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "",
        "address": "",
        "billing_address": "",
        "quantity": 1,
        "subtotal": format_amount_str(257.00),  # Sous-total initial
        "delivery_cost": format_amount_str(59.99),  # Frais de livraison initiaux
        "discount": format_amount_str(0.00),  # Réduction initiale
        "final_total": format_amount_str(316.99),  # Total initial
        "montant_total": format_amount_str(316.99),  # Montant total initial
        "note": "",
        "payment_method": "",
        "cardholder_name": "",
        "card_number": "",
        "expiry_date": "",
        "cvv": "",
        "installment_plan": "",
        "product_name": "Lot de 10 unités de foie gras Labeyrie 285g",
        "payment_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    print("Session initialisée :", session['order_data'])  # Log pour débogage
    return render_template('validation.html', data=session.get('order_data'))

# Route pour traiter la commande (GET et POST)
@app.route('/commander', methods=['GET', 'POST'])
def commander():
    if request.method == 'POST':
        # Récupérer et mettre à jour les données du formulaire
        order_data = session.get('order_data', {})
        print("Données du formulaire reçues :", request.form)  # Log pour débogage

        # Mettre à jour les données de la commande avec les valeurs du formulaire
        order_data.update({
            "first_name": request.form.get("first-name", ""),
            "last_name": request.form.get("last-name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "address": request.form.get("address", ""),
            "billing_address": request.form.get("billing-address", ""),
            "quantity": int(request.form.get("quantity", 1)),
            "subtotal": request.form.get("subtotal", "0,00 €"),
            "delivery_cost": request.form.get("delivery-cost", "0,00 €"),
            "discount": request.form.get("discount", "0,00 €"),
            "final_total": request.form.get("final-total", "0,00 €"),
            "note": request.form.get("note", ""),
            "payment_method": request.form.get("payment-method", ""),
        })

        # Convertir les montants en nombres pour les calculs
        order_data["subtotal"] = format_amount(order_data["subtotal"])
        order_data["delivery_cost"] = format_amount(order_data["delivery_cost"])
        order_data["discount"] = format_amount(order_data["discount"])
        order_data["final_total"] = format_amount(order_data["final_total"])

        # Recalculer le total si nécessaire
        order_data["final_total"] = order_data["subtotal"] + order_data["delivery_cost"] - order_data["discount"]

        # Synchroniser montant_total avec final_total
        order_data["montant_total"] = order_data["final_total"]

        # Mettre à jour les données dans la session
        session['order_data'] = order_data
        print("Données de commande mises à jour dans /commander :", session['order_data'])  # Log pour débogage

        # Rediriger vers /confirmation après la mise à jour des données
        return redirect(url_for('confirmation'))

    return render_template('confirmation.html', data=session.get('order_data'))

# Route pour la page de confirmation
@app.route('/confirmation')
def confirmation():
    # Récupérer les données de la session
    order_data = session.get('order_data', {})
    print("Données de la session dans /confirmation :", order_data)  # Log pour débogage

    if not order_data:
        print("Aucune donnée de commande trouvée dans la session. Redirection vers /commander.")  # Log pour débogage
        return redirect(url_for('commander'))  # Rediriger vers /commander

    return render_template('confirmation.html', data=order_data)

# Route pour le paiement en plusieurs fois
@app.route('/jumeler', methods=['GET', 'POST'])
def jumeler():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        order_data = {
            "first_name": request.form.get("first-name"),
            "last_name": request.form.get("last-name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "billing_address": request.form.get("billing-address"),
            "quantity": request.form.get("quantity"),
            "subtotal": request.form.get("subtotal"),
            "delivery_cost": request.form.get("delivery-cost"),
            "discount": request.form.get("discount"),
            "final_total": request.form.get("final-total"),
            "montant_total": request.form.get("montant-total"),
            "note": request.form.get("note"),
            "payment_method": request.form.get("payment-method"),
            "cardholder_name": request.form.get("cardholder-name"),
            "installment_plan": request.form.get("installment-plan"),
        }
        session['order_data'] = order_data  # Stocker les données dans la session
        return redirect(url_for('jumeler'))  # Rediriger vers jumeler.html

    # Récupérer les données de la session
    order_data = session.get('order_data', {})
    return render_template('jumeler.html', data=order_data)
# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(debug=True, port=5011)
