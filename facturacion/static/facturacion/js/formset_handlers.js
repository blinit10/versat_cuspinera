document.addEventListener('formset:added', (event) => {
    if (event.detail.formsetName == 'productos_factura') {
        // Do something
    }
});
document.addEventListener('formset:changed', (event) => {
    console.log(event.detail.formsetName)
    if (event.detail.formsetName == 'productos_factura') {
        // Do something
    }
});
document.addEventListener('formset:removed', (event) => {
    // Row removed
});

document.addEventListener('mousedown', ev => {
    const string = "".concat($(ev.target).attr('id'));
    const substring = "select2-id_productos_factura-";
    if (string.includes(substring)) {
        var operacion = $('#id_operacion').find(':selected').text()
        var sku = $(ev.target).html().toString().split(' - ')[0]
        var numero = $(ev.target).attr('id').toString().replace('select2-id_productos_factura-', '').replace('-producto-container', '')
        $.ajax({
            url: '/facturacion/precio/',
            data: {
                'modo': operacion,
                'sku':sku
            },
            success: function (response) {
                if (response['precio'] === -1){
                    alert("Operacion no definida")
                }else if (response['precio'] === -2){
                    alert("Operacion no permitida")
                }else{
                    $('#id_productos_factura-' + numero + '-precio').val(parseFloat(response['precio']))
                }

            },
        });

    }

});
