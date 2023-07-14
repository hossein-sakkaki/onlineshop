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
            status_of_compare_list()
        }
    })
}

function add_to_shop_cart(product_id, qty) {
    // alert(productId+' '+qty)
    $.ajax({
        type: 'GET',
        url: '/orders/add_to_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },
        success: function (res) {
            $('#indicator__value').text(res);
        }
    })
}