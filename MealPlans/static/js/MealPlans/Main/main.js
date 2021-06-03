(function(){
    let instance = JSON.parse(JSON.parse(document.getElementById("instance").textContent));
   window.clientStorage.setItem("instance",instance[0])
    document.getElementById("state").remove();
})();