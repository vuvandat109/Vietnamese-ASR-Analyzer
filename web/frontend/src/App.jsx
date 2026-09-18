import {
  useCallback,
  useEffect,
  useMemo,
  useState
} from "react";

import axios from "axios";

import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Legend
} from "recharts";

import "./App.css";



const API =
  import.meta.env.VITE_API_URL ??
  "http://127.0.0.1:8000";





const ERROR_LABELS = {

  tone_error:
  "Sai thanh điệu",

  nucleus_error:
  "Sai âm chính",

  initial_consonant_error:
  "Sai phụ âm đầu",

  final_consonant_error:
  "Sai âm cuối",

  missing_word:
  "Mất từ",

  merge_word:
  "Gộp từ",

  split_word:
  "Tách từ",

  extra_word:
  "Thêm từ"

};





function translateError(error){

  return ERROR_LABELS[error] ?? error;

}







const STATUS_MAP = {

  "Đúng":
  "correct",

  "Sai":
  "incorrect",

  "Lỗi phân tích":
  "failed",

  correct:
  "correct",

  incorrect:
  "incorrect",

  failed:
  "failed"

};





function getStatus(item){

  return STATUS_MAP[item.status] ?? "failed";

}





const STATUS_LABEL = {

  correct:
  "✓ Đúng",

  incorrect:
  "✗ Sai",

  failed:
  "⚠ Lỗi phân tích"

};








function formatPercent(value){

  const number =
  Number(value);


  if(
    !Number.isFinite(number)
  ){

    return "—";

  }


  return (

    number * 100

  ).toFixed(2) + "%";

}









function StatCard({

  title,

  value,

  className

}){


return (

<div className="card">


<h3>

{title}

</h3>



<strong className={className}>

{value ?? 0}

</strong>


</div>

);


}













function DetailModal({

  data,

  onClose

}){


return (

<div
className="drawer-overlay"
onClick={onClose}
>



<div
className="drawer"
onClick={
e=>e.stopPropagation()
}
>





<button

className="close-btn"

onClick={onClose}

>

X

</button>





<h2>

Chi tiết phân tích

</h2>





<h3>

Audio

</h3>


<p>

{data.audio}

</p>





<h3>

Câu chuẩn

</h3>



<div className="text-box">

{data.ground_truth}

</div>





<h3>

Whisper

</h3>



<div className="text-box">

{data.prediction}

</div>





<h3>

WER / CER

</h3>



<p>

{formatPercent(data.wer)}

{" / "}

{formatPercent(data.cer)}

</p>





<h3>

Phân loại lỗi

</h3>





{

Array.isArray(data.errors)

&&

data.errors.length > 0

?

data.errors.map(

(error,index)=>(


<span

key={index}

className="error-badge"

>

{translateError(error)}

</span>


)

)

:

<p>

Không có lỗi

</p>

}







{/* ============================
    PHONEME DETAIL FIXED
============================ */}



{

Array.isArray(data.word_analysis)

&&

data.word_analysis.length > 0

&&

(


<>


<h3>

Chi tiết lỗi phát âm

</h3>




{

Array.isArray(data.word_analysis)

&&

data.word_analysis.length > 0

&&

<section>

<h3>
Chi tiết lỗi phát âm
</h3>


<div>


{

data.word_analysis.map(

(item,index)=>(


<div

key={index}

className="alignment-card"

>


<div className="alignment-title">


<span className="reference-word">

{item.reference}

</span>


&nbsp; → &nbsp;


<span className="prediction-word">

{item.prediction}

</span>


</div>





<table className="phoneme-table">


<thead>

<tr>

<th>
Thành phần
</th>

<th>
Ground Truth
</th>

<th>
Whisper
</th>

<th>
Kết quả
</th>

</tr>

</thead>





<tbody>


<tr>

<td>
Âm đầu
</td>

<td>

{
item.detail?.initial?.reference ?? "-"
}

</td>

<td>

{
item.detail?.initial?.prediction ?? "-"
}

</td>


<td

className={

item.detail?.initial?.reference ===

item.detail?.initial?.prediction

?

"correct-cell"

:

"error-cell"

}

>

{

item.detail?.initial?.reference ===

item.detail?.initial?.prediction

?

"Đúng"

:

"Sai"

}

</td>


</tr>






<tr>

<td>
Âm chính
</td>

<td>

{
item.detail?.nucleus?.reference ?? "-"
}

</td>

<td>

{
item.detail?.nucleus?.prediction ?? "-"
}

</td>


<td

className={

item.detail?.nucleus?.reference ===

item.detail?.nucleus?.prediction

?

"correct-cell"

:

"error-cell"

}

>

{

item.detail?.nucleus?.reference ===

item.detail?.nucleus?.prediction

?

"Đúng"

:

"Sai"

}

</td>


</tr>






<tr>

<td>
Âm cuối
</td>

<td>

{
item.detail?.final?.reference || "-"
}

</td>

<td>

{
item.detail?.final?.prediction || "-"
}

</td>


<td

className={

item.detail?.final?.reference ===

item.detail?.final?.prediction

?

"correct-cell"

:

"error-cell"

}

>

{

item.detail?.final?.reference ===

item.detail?.final?.prediction

?

"Đúng"

:

"Sai"

}

</td>


</tr>







<tr>

<td>
Thanh điệu
</td>

<td>

{
item.detail?.tone?.reference || "-"
}

</td>


<td>

{
item.detail?.tone?.prediction || "-"
}

</td>


<td

className={

item.detail?.tone?.reference ===

item.detail?.tone?.prediction

?

"correct-cell"

:

"error-cell"

}

>

{

item.detail?.tone?.reference ===

item.detail?.tone?.prediction

?

"Đúng"

:

"Sai"

}

</td>


</tr>



</tbody>


</table>


</div>


)

)


}


</div>


</section>


}



</>

)


}




</div>


</div>


);


}
export default function App(){


const [

statistics,

setStatistics

] = useState(null);




const [

audioList,

setAudioList

] = useState([]);




const [

selected,

setSelected

] = useState(null);




const [

loading,

setLoading

] = useState(true);




const [

filter,

setFilter

] = useState("all");




const [

search,

setSearch

] = useState("");




const [

error,

setError

] = useState(null);








/* ============================
   LOAD DATA
============================ */


useEffect(()=>{


Promise.all([


axios.get(

`${API}/api/statistics`

),



axios.get(

`${API}/api/audio-list`

)



])


.then(([stat,audio])=>{


setStatistics(

stat.data

);



setAudioList(

audio.data.data ?? []

);



})


.catch((err)=>{


console.error(err);


setError(

"Không kết nối được backend"

);



})


.finally(()=>{


setLoading(false);



});



},[]);









/* ============================
   DETAIL AUDIO
============================ */


const openDetail =

useCallback(

async(audio)=>{


try{


const res =

await axios.get(

`${API}/api/audio-detail/${encodeURIComponent(audio)}`

);



setSelected(

res.data

);



}

catch(err){


console.error(err);


setError(

"Không tải được chi tiết audio"

);



}



},

[]



);









/* ============================
   ERROR CHART
============================ */


const chartData =

useMemo(()=>{


return Object.entries(

statistics?.error_distribution ?? {}

)

.map(

([key,value])=>(


{


name:

translateError(key),



value



}


)

);



},[statistics]);









/* ============================
   WER CER CHART
============================ */


const scoreData =

useMemo(()=>{


if(

!statistics?.score_chart

||

!Array.isArray(

statistics.score_chart

)

)

{


return [];

}



return statistics.score_chart.map(

(item)=>(



{


name:

item.audio

?

item.audio

.replace(

"common_voice_vi_",

""

)

.replace(

".mp3",

""

)

:

"unknown",





WER:

Number(

(item.wer ?? 0)

*

100

)

.toFixed(2),





CER:

Number(

(item.cer ?? 0)

*

100

)

.toFixed(2)



}



)



);



},[statistics]);









/* ============================
   FILTER DATA
============================ */


let tableData =

audioList;





if(

filter !== "all"

){


tableData =

tableData.filter(

item =>

getStatus(item)

===

filter

);



}






if(search.trim()){


tableData = tableData.filter(

item =>

(item.audio ?? "")

.toLowerCase()

.includes(

search.toLowerCase()

)

);


}








if(

loading

){


return (

<div className="loading">

Đang tải dữ liệu...

</div>

);


}









if(

!statistics

){


return (

<div className="loading">

{

error ??

"Không có dữ liệu"

}


</div>

);


}
return (

<div className="dashboard">



<h1>

Vietnamese ASR Error Analyzer

</h1>




<p className="subtitle">

Whisper Vietnamese Speech Recognition Dashboard

</p>
{
error && (

<div className="error-banner">

{error}

<button

onClick={()=>setError(null)}

>

×

</button>

</div>

)
}








<div className="cards">



<StatCard

title="Tổng Audio"

value={statistics.total_audio}

/>





<StatCard

title="Tổng lỗi"

value={statistics.total_error}

className="red"

/>





<StatCard

title="WER trung bình"

value={
formatPercent(
statistics.average_wer
)
}

/>





<StatCard

title="CER trung bình"

value={
formatPercent(
statistics.average_cer
)
}

/>





<StatCard

title="Corpus WER"

value={
formatPercent(
statistics.corpus_wer
)
}

/>





<StatCard

title="Câu đúng"

value={
statistics.correct_sentence
}

/>





<StatCard

title="Câu lỗi"

value={
statistics.incorrect_sentence
}

/>



</div>









{/* ============================
    ERROR DISTRIBUTION
============================ */}



<div className="section">


<h2>

Phân bố lỗi tiếng Việt

</h2>




<div className="chart-box">


{

chartData.length > 0

&&

(

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

)


}



</div>


</div>









{/* ============================
    WER CER CHART
============================ */}



<div className="section">


<h2>

WER / CER từng Audio

</h2>




<div className="chart-box">



{

scoreData.length > 0

&&

(

<ResponsiveContainer

width="100%"

height="100%"

>


<BarChart

data={scoreData}

>


<XAxis

dataKey="name"

angle={-30}

height={80}

/>



<YAxis/>




<Tooltip/>





<Legend/>

<Bar

dataKey="WER"

fill="#2563eb"

/>


<Bar

dataKey="CER"

fill="#dc2626"

/>



</BarChart>


</ResponsiveContainer>

)



}



</div>


</div>









{/* ============================
    AUDIO TABLE
============================ */}



<div className="section">


<h2>

Danh sách Audio

</h2>





<input


className="search"


placeholder="Tìm audio..."


value={search}



onChange={

e=>setSearch(

e.target.value

)

}


/>









<div className="filter">


<button

className={

filter==="all"

?

"active"

:

""

}


onClick={

()=>setFilter("all")

}

>

Tất cả

</button>







<button

className={

filter==="incorrect"

?

"active"

:

""

}


onClick={

()=>setFilter("incorrect")

}

>

Có lỗi

</button>







<button

className={

filter==="correct"

?

"active"

:

""

}


onClick={

()=>setFilter("correct")

}

>

Đúng

</button>



</div>









<table>


<thead>


<tr>


<th>

Audio

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

(item)=>(



<tr

key={item.audio}

onClick={

()=>openDetail(item.audio)

}

>



<td>

{item.audio}

</td>






<td>

{formatPercent(item.wer)}

</td>






<td>

{formatPercent(item.cer)}

</td>







<td>

<span

className={

getStatus(item)==="correct"

?

"status-good"

:

getStatus(item)==="incorrect"

?

"status-bad"

:

"status-failed"

}

>

{

STATUS_LABEL[getStatus(item)]

}

</span>

</td>






<td>



{

Array.isArray(item.errors)

&&

item.errors.map(

(error,index)=>(


<span

key={index}

className="error-badge"

>


{

translateError(error)

}



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









{/* ============================
    DETAIL MODAL
============================ */}




{

selected

&&



<DetailModal


data={selected}



onClose={

()=>setSelected(null)

}


/>



}



</div>


);



}