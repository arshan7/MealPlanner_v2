
function AjaxHandler({request_location, data = null, method = "GET",
                         token = {header:null, value:null},handler = null}) {
    return new Promise((resolve,reject)=>{
    let response ='';
    try {
        if (request_location === null || request_location === undefined)
            throw "Request location not supplied";
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (handler != null) {
                    handler(xhr.responseText);
                    resolve(response);
                }
            }
        };
        if(method.toUpperCase()==="GET")
            request_location+=data!= null?data:"";
        xhr.open(method, request_location);
        if(method.toUpperCase()==="POST")
        xhr.setRequestHeader(token.header,token.value)
        xhr.send(data);

    } catch (err) {
        console.log("request can't be processed", err);
    }
    });
}