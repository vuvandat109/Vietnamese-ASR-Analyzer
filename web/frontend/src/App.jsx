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


const [report,setReport]=useState(null);

const [analysis,setAnalysis]=useState([]);

const [loading,setLoading]=useState(true);



useEffect(()=>{


axios
.get("http://127.0.0.1:8000/report")
.then(res=>{

setReport(res.data);

});



axios
.get("http://127.0.0.1:8000/analysis")
.then(res=>{


setAnalysis(
res.data.data || []
);


setLoading(false);


});


},[]);




if(loading || !report){

return (

<h2>
Đang tải dữ liệu...
</h2>

)

}



const tongQuan =
report.tong_quan;



const loi =
report.phan_tich_loi_tieng_viet;



const chartData =
Object
.entries(loi)
.map(
([name,value])=>({

name,
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
Số Audio
</h3>

<strong>
{tongQuan.so_luong_audio}
</strong>

</div>



<div className="card">

<h3>
WER
</h3>

<strong>
{
(tongQuan.WER_trung_binh*100)
.toFixed(2)
}%

</strong>

</div>



<div className="card">

<h3>
CER
</h3>

<strong>

{
(tongQuan.CER_trung_binh*100)
.toFixed(2)
}%

</strong>

</div>



</div>





<div className="section">

<h2>
Phân tích lỗi tiếng Việt
</h2>


<div className="chart-box">


<ResponsiveContainer
width="100%"
height="100%"
>


<BarChart
data={chartData}
>


<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Bar dataKey="value"/>


</BarChart>


</ResponsiveContainer>


</div>


</div>







<div className="section">


<h2>
Phân tích theo Audio
</h2>



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
Lỗi
</th>

</tr>


</thead>



<tbody>


{

analysis.map(
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
item.errors.map(
(e,i)=>(

<div key={i}>

{e}

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