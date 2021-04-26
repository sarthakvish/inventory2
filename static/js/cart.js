var updateBtns=document.getElementsByClassName('update-cart');
//html to javascript to url.py to veiw.py is the flow
for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function(ev){
        var el = ev.target;
        var productId=el.dataset.product
        var action=el.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log("USER:", user)
        if(user==='AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
            var url='/update_item/'
            fetch(url,{
                method:'POST',
                headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken,},
                body:JSON.stringify({'productId':productId,'action':action})
            })

               .then((response) => {
                   return response.json()
            })

            .then((data)=>{
                console.log('data:', data);
                location.reload()
            })

        }

})
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data')
}