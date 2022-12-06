from js import document, console
import json
from pyodide import create_proxy
from pyodide.http import pyfetch
from itertools import count
import pandas as pd


# def load_json_file(path):
#     """ no funciona"""
#     with open(path, 'r') as f:
#         return json.load(f)

def read_json():
    json_data = """
[
    {
        "precio": 500,
        "id": 1,
        "title": "Café",
        "thumbnailUrl": "https://picsum.photos/id/0/600"
        },
    {
        "precio": 300,
        "id": 2,
        "title": "Pizza",
        "thumbnailUrl": "https://picsum.photos/id/10/600"
        },
    {
        "precio": 100,
        "id": 3,
        "title": "Agua",
        "thumbnailUrl": "https://picsum.photos/id/20/600"
        },
    {
        "precio": 50,
        "id": 4,
        "title": "Sandía",
        "thumbnailUrl": "https://picsum.photos/id/30/600"
        },
    {
        "precio": 10,
        "id": 5,
        "title": "Mango",
        "thumbnailUrl": "https://picsum.photos/id/40/600"
        },
    {
        "precio": 150,
        "id": 6,
        "title": "Chela",
        "thumbnailUrl": "https://picsum.photos/id/50/600"
    }
]
"""
    return json.loads(json_data)

def fetchData(log=False):
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a fetchData")
    try:
        # response = load_json_file("./api.json")
        response = read_json()
        data = json.dumps(response, indent=2)
        if log: console.log(f"\n\tlog_[{next(x)}]\n{data}")
        return response
    except Exception as error:
        console.log(error)

def pintarCards(data, log=False):
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a pintarCards")
    fragment = document.createDocumentFragment()
    for producto in data:
        if log: console.log(f"\n\tlog_[{next(x)}]\n{str(producto)}")
        ### IMPORTANTE
        templateCard.querySelector('h5').textContent = producto['title']
        templateCard.querySelector('p').textContent = producto['precio']
        templateCard.querySelector('img').setAttribute('src', producto['thumbnailUrl'])
        templateCard.querySelector('.btn-dark').dataset.id = producto['id']

        clone = templateCard.cloneNode(True)
        fragment.appendChild(clone)
        ###
    items.appendChild(fragment)

def addCarrito(e, log=False):
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a addCarrito")
    if log: console.log(f"\n\tlog_[{next(x)}]");console.log(e.target)
    
    ### IMPORTANTE
    if e.target.classList.contains('btn-dark'):
        if log: console.log(f"\n\tlog_[{next(x)}]");console.log(e.target.parentElement)
        setCarrito(e.target.parentElement, log=True)
    
    e.stopPropagation()



def setCarrito(objeto, log=False):
    """modificar el objeto Carrito"""
    global x, Carrito

    Carrito = pd.concat([Carrito, pd.DataFrame(columns=['id', 'title', 'precio', 'cantidad'])])


    def add_row(df, objeto, log=log):
        """agregar una fila al objeto Carrito"""
        if log: console.log(f"\n\tlog_[{next(x)}]\nIngresando a add_row")
        row = pd.DataFrame(objeto, index=[list(objeto.keys())[0]])
        return pd.concat([df, row])


    console.log(f"\n\tlog_[{next(x)}]\nIngresando a setCarrito")
    if log: console.log(f"\n\tlog_[{next(x)}]");console.log(objeto)


    producto = {
        'id': objeto.querySelector('.btn-dark').dataset.id,
        'title': objeto.querySelector('h5').textContent,
        'precio': objeto.querySelector('p').textContent,
        'cantidad': 1
    }

    if log: console.log(f"\n\tlog_[{next(x)}]");console.log(json.dumps(producto))

    if Carrito.id.isin([producto[list(producto.keys())[0]]]).any():
        console.log(f"\n\tlog_[{next(x)}]\nYa existe el producto en el carrito")
        Carrito.loc[Carrito.id == producto['id'], 'cantidad'] += 1
    else:
        console.log(f"\n\tlog_[{next(x)}]\nSe crea el producto en el carrito")
        Carrito = add_row(Carrito, producto)

    producto['cantidad'] = Carrito.loc[Carrito.id == producto['id'], 'cantidad'].values[0]
    if log: console.log(f"\n\tlog_[{next(x)}]");console.log(str(producto))

    pintarCarrito(log=log)


def pintarCarrito(log=False):
    global x, Carrito, templateCarrito, compras

    fragment = document.createDocumentFragment()
    compras.innerHTML = ''
    
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a pintarCarrito")
    console.log(Carrito.to_json(orient='records'))
    for i in range(len(Carrito)):
        objeto = Carrito.iloc[i].to_frame().T
        templateCarrito.querySelector('th').textContent = objeto['id'].values[0]
        templateCarrito.querySelectorAll('td')[0].textContent = objeto['title'].values[0]
        templateCarrito.querySelectorAll('td')[1].textContent = objeto['cantidad'].values[0]
        templateCarrito.querySelector(".btn-info").dataset.id = objeto['id'].values[0]
        templateCarrito.querySelector(".btn-danger").dataset.id = objeto['id'].values[0]
        templateCarrito.querySelector('span').textContent = objeto['cantidad'].values[0] * int(objeto['precio'].values[0])

        clone = templateCarrito.cloneNode(True)
        fragment.appendChild(clone)

    compras.appendChild(fragment)

    pintarFooter(log=log)

def pintarFooter(log=False):
    global x, Carrito, footer, templateFooter

    fragment = document.createDocumentFragment()

    console.log(f"\n\tlog_[{next(x)}]\nIngresando a pintarFooter")
    footer.innerHTML = ''

    if Carrito.shape[0] == 0:
        footer.innerHTML = """
        <th scope="row" colspan="5">Carrito vacío - comience a comprar!</th>
        """
        return

    total = 0
    for i in range(len(Carrito)):
        objeto = Carrito.iloc[i].to_frame().T
        total += objeto['cantidad'].values[0] * int(objeto['precio'].values[0])

    cantidad = Carrito['cantidad'].sum()

    templateFooter.querySelectorAll('td')[0].textContent = cantidad
    templateFooter.querySelector('span').textContent = total
    clone = templateFooter.cloneNode(True)
    fragment.appendChild(clone)

    footer.appendChild(fragment)


    btnVaciar = document.getElementById('vaciar-carrito')
    btnVaciar.addEventListener('click', create_proxy(vaciarCarrito))

def vaciarCarrito(e):
    global x, Carrito
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a vaciarCarrito")
    Carrito = pd.DataFrame(columns=['id', 'title', 'precio', 'cantidad'])
    pintarCarrito()


def btnCantidad(e):
    global x, Carrito
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a btnCantidad")
    console.log(e.target)
    if e.target.classList.contains('btn-info'):
        console.log(f"\n\tlog_[{next(x)}]\nAumentando cantidad")
        Carrito.loc[Carrito.id == e.target.dataset.id, 'cantidad'] += 1
        pintarCarrito()
    elif e.target.classList.contains('btn-danger'):
        console.log(f"\n\tlog_[{next(x)}]\nDisminuyendo cantidad")
        Carrito.loc[Carrito.id == e.target.dataset.id, 'cantidad'] -= 1
        if Carrito.loc[Carrito.id == e.target.dataset.id, 'cantidad'].values[0] == 0:
            console.log(f"\n\tlog_[{next(x)}]\nEliminando producto")
            Carrito = Carrito[Carrito.id != e.target.dataset.id]
        pintarCarrito()

    e.stopPropagation()

def main():
    # se crean en el HTML
    global templateCard, items, templateFooter, templateCarrito, compras, footer
    # se crean localmente
    global x, Carrito
    x = count(1)
    Carrito = pd.DataFrame()

    console.log(f"\n\tlog_[{next(x)}]\nIngresando al main")


    data = fetchData()
    templateCard = document.getElementById('template-card').content
    items = document.getElementById('items')
    templateFooter = document.getElementById('template-footer').content
    templateCarrito = document.getElementById('template-carrito').content
    compras = document.getElementById('compras')
    footer = document.getElementById('footer')


    pintarCards(data)

    items.addEventListener('click', create_proxy(addCarrito))

    compras.addEventListener('click', create_proxy(btnCantidad))

    # document.addEventListener("DOMContentLoaded", pyodide.create_proxy(fetchData))


main()
