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


function App() {


  const [report, setReport] = useState(null);

  const [analysis, setAnalysis] = useState([]);

  const [filter, setFilter] = useState("all");

  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);



  useEffect(() => {


    axios
      .get("http://127.0.0.1:8000/report")
      .then(res => {

        setReport(res.data);

      });



    axios
      .get("http://127.0.0.1:8000/analysis")
      .then(res => {


        setAnalysis(
          res.data.data || []
        );


        setLoading(false);

      });


  }, []);




  if(
    loading ||
    !report
  ){

    return (

      <div className="loading">

        Đang tải dữ liệu...

      </div>

    );

  }





  // =============================
  // THỐNG KÊ
  // =============================


  const totalAudio =
    analysis.length;



  const correct =
    analysis.filter(
      item =>
      item.status === "Đúng"
    ).length;



  const wrong =
    analysis.filter(
      item =>
      item.status === "Sai"
    ).length;



  const avgWER =
    (
      report.tong_quan.WER_trung_binh
      *
      100
    )
    .toFixed(2);



  const avgCER =
    (
      report.tong_quan.CER_trung_binh
      *
      100
    )
    .toFixed(2);





  // =============================
  // DỊCH LỖI
  // =============================


  function translateError(error){


    const map = {


      tone_error:
      "Sai thanh điệu",


      initial_consonant_error:
      "Sai phụ âm đầu",


      final_consonant_error:
      "Sai âm cuối",


      nucleus_error:
      "Sai âm chính",


      multi_component_error:
      "Sai nhiều thành phần",


      non_vietnamese_token:
      "Token ngoài tiếng Việt"


    };


    return map[error] || error;


  }





  // =============================
  // FILTER DATA
  // =============================


  let tableData = analysis;



  if(filter==="wrong"){


    tableData =
      tableData.filter(
        item =>
        item.status==="Sai"
      );


  }



  if(filter==="correct"){


    tableData =
      tableData.filter(
        item =>
        item.status==="Đúng"
      );


  }




  if(search.trim()){


    tableData =
      tableData.filter(
        item =>


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





  // =============================
  // ERROR CHART
  // =============================


  const errorCount = {};



  analysis.forEach(item=>{


    item.errors.forEach(error=>{


      errorCount[error] =
      (
        errorCount[error] || 0
      )
      +1;


    });


  });



  const chartData =

    Object
    .entries(errorCount)
    .map(
      ([name,value])=>({

        name:
        translateError(name),

        value,

        percent:
        (
          value /
          analysis.length *
          100
        )
        .toFixed(1)

      })
    );





  return (

<div className="dashboard">


<h1>
Vietnamese ASR Error Analyzer
</h1>


<p className="subtitle">
Whisper Vietnamese Speech Recognition Evaluation Dashboard
</p>





<div className="cards">



<div className="card">

<h3>
Tổng Audio
</h3>

<strong>
{totalAudio}
</strong>

</div>





<div className="card">

<h3>
Nhận dạng đúng
</h3>

<strong className="green">

{correct}

</strong>

</div>





<div className="card">

<h3>
Có lỗi
</h3>

<strong className="red">

{wrong}

</strong>

</div>





<div className="card">

<h3>
WER / CER
</h3>

<strong>

{avgWER}% / {avgCER}%

</strong>

</div>




</div>
// =============================
// ERROR CHART
// =============================


<div className="section">


<h2>
Phân bố lỗi tiếng Việt
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


<Tooltip
formatter={
(value,name,item)=>[
`${value} lỗi (${item.payload.percent}%)`,
"Lỗi"
]
}
/>


<Bar
dataKey="value"
/>


</BarChart>


</ResponsiveContainer>


</div>


</div>





{/* =============================
    TABLE ANALYSIS
============================= */}



<div className="section">


<h2>
Phân tích từng Audio
</h2>




<div className="filter">


<button
onClick={() =>
setFilter("all")
}
>
Tất cả
</button>



<button
onClick={() =>
setFilter("wrong")
}
>
Chỉ lỗi
</button>



<button
onClick={() =>
setFilter("correct")
}
>
Chính xác
</button>


</div>





<input

className="search"

placeholder="Tìm kiếm câu nhận dạng..."

value={search}

onChange={
e =>
setSearch(e.target.value)
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
WER
</th>


<th>
CER
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

tableData.map(

(item,index)=>(


<tr
key={index}
>




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

item.wer !== undefined

?

(
item.wer * 100
)
.toFixed(2)
+

"%"

:

"-"

}

</td>






<td>

{

item.cer !== undefined

?

(
item.cer * 100
)
.toFixed(2)
+

"%"

:

"-"

}

</td>







<td>


<span

className={

item.status==="Đúng"

?

"status-good"

:

"status-bad"

}

>


{

item.status==="Đúng"

?

"✓ Đúng"

:

"✗ Sai"

}


</span>



</td>







<td>


{

item.errors.length===0

?


<span className="success">

Không lỗi

</span>


:


item.errors.map(

(error,i)=>(


<span

key={i}

className="error-badge"

>

{translateError(error)}

</span>


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