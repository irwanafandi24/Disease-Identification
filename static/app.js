function onClickedAnalysis(){
    console.log("Start to Analyst Plant Leaf");
    var landArea = document.getElementById("uiLandArea");
    var minimumPrice = document.getElementById("uiMinimumPrice");
    var maximumPrice = document.getElementById("uiMaximumPrice");
    var leafImage = document.getElementById("uiImage");
    var predictionResult = document.getElementById("prediction_result");
    var diseaseInfo = document.getElementById("disease_info");
    var diseaseTreatment = document.getElementById("disease_treatment");
    var recommendationTable = document.getElementById("dataTable");
    var temp = "";
    var idx = 0;

    const endpoint = "http://127.0.0.1:5000/leaf_analysis";
    const formData = new FormData();

    formData.append('landArea', parseInt(landArea.value));
    formData.append('minimumPrice', parseInt(minimumPrice.value));
    formData.append('maximumPrice', parseInt(maximumPrice.value));
    formData.append('leafImage', leafImage.files[0])

    fetch(endpoint, {
        method : "post",
        body:formData
    })
    .then(response => response.json())
    .then(data =>{
        predictionResult.innerHTML = "<h2 class='text-result'>"+data.disease_result.toString()+"</h2>",
        diseaseInfo.innerHTML = "<p>"+data.disease_info.toString()+"</p>",
        diseaseTreatment.innerHTML = "<p>"+data.treatment_info+"</p>",
        data.recommendation.forEach((u)=>{
            idx++;
            temp += "<tr>";
            temp += "<td>"+idx.toString()+"</td>";
            temp += "<td>"+u.pesticide+"</td>";
            temp += "<td>"+u.price+"</td>";
            temp += "<td>"+u.need+"</td>";
            temp += "<td><a href='"+u.url_store+"' target='_blank'>"+u.store+"</a></td>";
            temp += "</tr>";
        })
        recommendationTable.innerHTML = temp;
    });
    console.log("done process")
}

//https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch