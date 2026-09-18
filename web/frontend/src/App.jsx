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
  YAxis
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



function translateError(e){

  return ERROR_LABELS[e] ?? e;

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

  const number = Number(value);


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
      className="modal-overlay"
      onClick={onClose}
    >


      <div

        className="modal"

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

          data.errors?.length === 0

          ?

          <p>
            Không có lỗi
          </p>

          :

          data.errors.map(
            (e,index)=>(

              <span

                key={index}

                className="error-badge"

              >

                {translateError(e)}

              </span>

            )

          )

        }








        {
          data.word_analysis &&

          data.word_analysis.length > 0 &&


          <>

          <h3>
            Chi tiết lỗi phát âm
          </h3>



          {
            data.word_analysis.map(
              (item,index)=>(


                <div

                  key={index}

                  className="word-card"

                >


                  <b>

                    {item.reference}

                    {" → "}

                    {item.prediction}

                  </b>



                  {

                    item.detail &&

                    <div>


                      <p>

                      Âm đầu:

                      {" "}

                      {
                        item.detail.initial.reference
                      }

                      {" → "}

                      {
                        item.detail.initial.prediction
                      }


                      </p>



                      <p>

                      Âm chính:

                      {" "}

                      {
                        item.detail.nucleus.reference
                      }

                      {" → "}

                      {
                        item.detail.nucleus.prediction
                      }


                      </p>



                      <p>

                      Âm cuối:

                      {" "}

                      {
                        item.detail.final.reference || "-"
                      }

                      {" → "}

                      {
                        item.detail.final.prediction || "-"
                      }


                      </p>



                      <p>

                      Thanh điệu:

                      {" "}

                      {
                        item.detail.tone.reference
                      }

                      {" → "}

                      {
                        item.detail.tone.prediction
                      }


                      </p>


                    </div>


                  }



                </div>


              )

            )

          }


          </>

        }



      </div>


    </div>

  );

}









export default function App(){



const [statistics,setStatistics]
=
useState(null);



const [audioList,setAudioList]
=
useState([]);



const [selected,setSelected]
=
useState(null);



const [loading,setLoading]
=
useState(true);



const [filter,setFilter]
=
useState("all");



const [search,setSearch]
=
useState("");



const [error,setError]
=
useState(null);







useEffect(()=>{


Promise.all([

axios.get(
`${API}/api/statistics`
),

axios.get(
`${API}/api/audio-list`
)

])


.then(([s,a])=>{


setStatistics(
s.data
);


setAudioList(
a.data.data ?? []
);


})


.catch(()=>{


setError(
"Không tải được dữ liệu backend"
);


})


.finally(()=>{


setLoading(false);


});


},[]);







const openDetail =
useCallback(async(audio)=>{


try{


const res =
await axios.get(

`${API}/api/audio-detail/${encodeURIComponent(audio)}`

);


setSelected(
res.data
);


}

catch(e){

console.log(e);

}


},[]);







let tableData =
audioList;



if(filter!=="all"){


tableData =
tableData.filter(

x=>

getStatus(x)===filter

);


}





if(search.trim()){


tableData =
tableData.filter(

x=>

x.audio
.toLowerCase()
.includes(
search.toLowerCase()
)

);


}







const chartData =
useMemo(()=>{


return Object.entries(

statistics?.error_distribution ?? {}

)

.map(([key,value])=>({

name:
translateError(key),

value

}));


},[statistics]);







if(loading){


return (

<div className="loading">

Đang tải dữ liệu...

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





<div className="cards">


<StatCard

title="Tổng Audio"

value={
statistics.total_audio
}

/>



<StatCard

title="Tổng lỗi"

value={
statistics.total_error
}

className="red"

/>



</div>








<div className="section">


<h2>
Phân bố lỗi
</h2>


<div className="chart-box">


<ResponsiveContainer

width="100%"

height="100%"

>


<BarChart data={chartData}>


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
Danh sách Audio
</h2>



<input

className="search"

placeholder="Tìm audio..."

value={search}

onChange={
e=>setSearch(e.target.value)
}

/>




<div className="filter">


<button onClick={()=>setFilter("all")}>
Tất cả
</button>


<button onClick={()=>setFilter("incorrect")}>
Có lỗi
</button>


<button onClick={()=>setFilter("correct")}>
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

tableData.map(item=>(


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

{
STATUS_LABEL[getStatus(item)]
}

</td>



<td>


{
item.errors?.map(

(e,i)=>(

<span

key={i}

className="error-badge"

>

{translateError(e)}

</span>

)

)

}



</td>


</tr>


))

}


</tbody>


</table>


</div>







{
selected &&

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