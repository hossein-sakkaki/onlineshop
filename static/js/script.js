function status_of_compare_list() {
    $.ajax({
        type: 'GET',
        url: '/products/status_of_compare_list/',
        success: function (res) {
            if (Number(res) === 0) {
                $('#compare_count_icon').hide();
            } else {
                $('#compare_count_icon').show();
                $('#compare_count').text(res);

            }
            
        }
    })

}

function addToCompareList(productId, productGroupId) {
    $.ajax({
        type: 'GET',
        url: '/products/add_to_compare_list',
        data: {
            productId: productId,
            productGroupId: productGroupId
        },
        success: function (res) {
            alert(res);
            status_of_compare_list()
        }
    })
}

function deleteFromCompareList(productId) {
    $.ajax({
        type: "GET",
        url: '/products/delete_from_compare_list/',
        data: {
            productId: productId,
        },
        success: function (res) {
            alert('Deleted...!');
            $('#compare_list').html(res);
            status_of_compare_list();
        }
    })
}

// choice product sort
function select_sort() {
    var select_sort_value = $('#select_sort').val();
    var url = removeURLParameter(window.location.href, 'sort_type');
    window.location = url + '&sort_type=' + select_sort_value;
}

// shop cart
function status_of_shop_cart() {
    $.ajax({
        type: 'GET',
        url: '/orders/status_of_shop_cart/',
        success: function (res) {
            $('#indicator__value').text(res);
        }
    })
}
status_of_shop_cart()

function add_to_shop_cart(product_id, qty) {
    if (qty === 0) {
        qty = $('#product-quantity').val();
    }
    $.ajax({
        type: 'GET',
        url: '/orders/add_to_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },
        success: function (res) {
            alert('Product was add to shop cart');
            status_of_shop_cart();
        }
    })
}

function delete_from_shop_cart(product_id) {
    $.ajax({
        type: 'GET',
        url: '/orders/delete_from_shop_cart/',
        data: {
            product_id: product_id,
        },
        success: function (res) {
            alert('Product was delete from shop cart');
            $('#shop_cart_list').html(res);
            status_of_shop_cart();
        }
    })
}

function update_shop_cart() {
    alert('test');
    var product_id_list = []
    var qty_list = []
    $('input[id^="qty_"]').each(function (index) {
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    $.ajax({
        type: 'GET',
        url: '/orders/update_shop_cart/',
        data: {
            product_id_list: product_id_list,
            qty_list: qty_list,
        },
        success: function (res) {
            alert('yes');
            $('#shop_cart_list').html(res);
            status_of_shop_cart();
        }
    }) 
}