from flask_injector import inject
from shiny_flask_app.providers.CouchProvider import CouchProvider


@inject
def create_product(productPayload, data_provider=CouchProvider()) -> str:
    return data_provider.create_product(productPayload)


@inject
def read_product(prod_id, data_provider=CouchProvider()) -> str:
    return data_provider.read_product(prod_id)


@inject
def update_product(productPayload, data_provider=CouchProvider()) -> str:
    return data_provider.update_product(productPayload)


@inject
def delete_product(prod_id, data_provider=CouchProvider()) -> str:
    return data_provider.delete_product(prod_id)
