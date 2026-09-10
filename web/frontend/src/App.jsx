import { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import "./App.css";


function App(){


const [report,setReport] = useState(null);

const [analysis,setAnalysis] = useState([]);

const [filter,setFilter] = useState("all");

const [search,setSearch] = useState("");

const [loading,setLoading] = useState(true);





// =========================
// LOAD DATA
// =========================

useEffect(()=>{


axios
.get(
"http://127.0.0.1:8000/report"
)

.then(res=>{

setReport(res.data);

});



axios
.get(
"http://127.0.0.1:8000/analysis"
)

.then(res=>{

setAnalysis(
res.data.data || []
);


setLoading(false);


});


},[]);





if(
loading ||
!report
){

return (

<h2>
Đang tải dữ liệu...
</h2>

)

}





// =========================
// THỐNG KÊ
// =========================


const total =
analysis.length;



const correct =
analysis.filter(
item=>item.status==="Đúng"
)
.length;



const wrong =
analysis.filter(
item=>item.status==="Sai"
)
.length;





// =========================
// DỊCH LỖI
// =========================


function translateError(error){


const map={


"tone_error":
"Sai thanh điệu",


"initial_consonant_error":
"Sai phụ âm đầu",


"final_consonant_error":
"Sai âm cuối",


"nucleus_error":
"Sai âm chính",


"multi_component_error":
"Sai nhiều thành phần",


"non_vietnamese_token":
"Token không phải tiếng Việt"


};


return map[error] || error;


}





// =========================
// FILTER
// =========================


let filtered =
analysis;



if(
filter==="correct"
){

filtered =
filtered.filter(
item=>item.status==="Đúng"
)

}



if(
filter==="wrong"
){

filtered =
filtered.filter(
item=>item.status==="Sai"
)

}





if(search.trim()!==""){


filtered =
filtered.filter(item=>

item.ground_truth
.toLowerCase()
.includes(
search.toLowerCase()
)

||
item.prediction
.toLowerCase()
.includes(
search.toLowerCase()
)


);


}






// =========================
// BIỂU ĐỒ
// =========================


const errorCount={};


analysis.forEach(item=>{


item.errors.forEach(error=>{


errorCount[error] =
(errorCount[error] || 0)+1;


});


});



const chartData = Object
.entries(errorCount)
.map(
([name,value])=>({

name:
translateError(name),

value

})
);





return (


<div className="dashboard">


<h1>
Vietnamese ASR Error Analyzer
</h1>


<p className="subtitle">
Whisper Vietnamese Speech Recognition Evaluation
</p>




<div className="cards">


<div className="card">

<h3>
Tổng Audio
</h3>

<strong>
{total}
</strong>

</div>




<div className="card">

<h3>
Đúng
</h3>

<strong>
{correct}
</strong>

</div>




<div className="card">

<h3>
Sai
</h3>

<strong>
{wrong}
</strong>

</div>



<div className="card">

<h3>
WER
</h3>

<strong>

{
(
report.tong_quan.WER_trung_binh
*
100
)
.toFixed(2)
}%

</strong>


</div>


</div>





<div className="section">


<h2>
Thống kê lỗi tiếng Việt
</h2>



<div className="chart-box">


<ResponsiveContainer
width="100%"
height="100%"
>


<BarChart
data={chartData}
>


<XAxis
dataKey="name"
/>


<YAxis/>


<Tooltip/>


<Bar
dataKey="value"
/>


</BarChart>


</ResponsiveContainer>


</div>


</div>







<div className="section">


<h2>
Phân tích từng Audio
</h2>



<div>


<button
onClick={()=>setFilter("all")}
>
Tất cả
</button>


<button
onClick={()=>setFilter("wrong")}
>
Chỉ lỗi
</button>


<button
onClick={()=>setFilter("correct")}
>
Chính xác
</button>


</div>




<br/>


<input

placeholder="Tìm kiếm câu..."

value={search}

onChange={
e=>setSearch(e.target.value)
}

/>





<table>


<thead>

<tr>

<th>
Audio
</th>

<th>
Câu chuẩn
</th>

<th>
Whisper
</th>

<th>
Trạng thái
</th>

<th>
Lỗi
</th>


</tr>

</thead>




<tbody>


{
filtered.map(
(item,index)=>(


<tr key={index}>


<td>
{item.audio}
</td>


<td>
{item.ground_truth}
</td>


<td>
{item.prediction}
</td>



<td>

{
item.status==="Đúng"
?
"✅ Đúng"
:
"❌ Sai"
}


</td>




<td>


{
item.errors.length===0

?

"Không lỗi"

:

item.errors.map(
(e,i)=>(

<div key={i}>

{translateError(e)}

</div>

)

)

}



</td>



</tr>


)

)

}



</tbody>


</table>



</div>



</div>


);


}


export default App;