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