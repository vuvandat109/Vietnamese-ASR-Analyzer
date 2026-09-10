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

  const [errors, setErrors] = useState([]);



  // ============================
  // LẤY DỮ LIỆU BACKEND
  // ============================

  useEffect(() => {


    axios
      .get(
        "http://127.0.0.1:8000/report"
      )
      .then((res)=>{

        setReport(res.data);

      })
      .catch((err)=>{

        console.log(
          "Lỗi lấy report:",
          err
        );

      });



    axios
      .get(
        "http://127.0.0.1:8000/errors"
      )
      .then((res)=>{


        console.log(
          "ERROR DATA:",
          res.data
        );


        setErrors(
          res.data.data || []
        );


      })
      .catch((err)=>{


        console.log(
          "Lỗi lấy errors:",
          err
        );


      });



  }, []);




  if(!report){

    return (

      <h2>
        Đang tải dữ liệu...
      </h2>

    );

  }



  const tongQuan =
    report.tong_quan;



  // ============================
  // DỮ LIỆU BIỂU ĐỒ
  // ============================


  const loiTiengViet =
    report.phan_tich_loi_tieng_viet;



  const chartData = Object
    .entries(loiTiengViet)
    .map(
      ([name,value])=>({

        name,

        value

      })
    );





  // ============================
  // HÀM LẤY GIÁ TRỊ AN TOÀN
  // ============================


  function getValue(
    item,
    keys
  ){

    for(
      let key of keys
    ){

      if(
        item[key] !== undefined
      ){

        return item[key];

      }

    }


    return "";

  }





  return (


    <div className="dashboard">


      <h1>
        Vietnamese ASR Error Analyzer
      </h1>


      <p className="subtitle">
        Whisper Vietnamese Speech Recognition Evaluation
      </p>





      {/* ================= CARD ================= */}


      <div className="cards">


        <div className="card">

          <h3>
            Số Audio
          </h3>

          <strong>
            {
              tongQuan.so_luong_audio
            }
          </strong>


        </div>





        <div className="card">

          <h3>
            WER
          </h3>


          <strong>

            {
              (
                tongQuan.WER_trung_binh
                *
                100
              )
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
              (
                tongQuan.CER_trung_binh
                *
                100
              )
              .toFixed(2)
            }%

          </strong>


        </div>



      </div>







      {/* ================= BIỂU ĐỒ ================= */}


      <div className="section">


        <h2>
          Phân tích lỗi tiếng Việt
        </h2>


        <div
          className="chart-box"
        >


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


              <YAxis />


              <Tooltip />


              <Bar
                dataKey="value"
              />


            </BarChart>


          </ResponsiveContainer>


        </div>


      </div>








      {/* ================= BẢNG LỖI ================= */}



      <div className="section">


        <h2>
          Chi tiết lỗi nhận dạng
        </h2>



        <table>


          <thead>

            <tr>

              <th>
                Từ chuẩn
              </th>


              <th>
                Whisper nhận dạng
              </th>


              <th>
                Loại lỗi
              </th>


            </tr>


          </thead>





          <tbody>


          {


            errors.map(

              (item,index)=>(



                <tr
                  key={index}
                >



                  <td>

                    {
                      getValue(
                        item,
                        [
                          "reference",
                          "REF",
                          "ref",
                          "tu_dung",
                          "word"
                        ]
                      )
                    }


                  </td>




                  <td>


                    {
                      getValue(
                        item,
                        [
                          "hypothesis",
                          "HYP",
                          "hyp",
                          "asr_nhan_dang",
                          "prediction"
                        ]
                      )
                    }


                  </td>





                  <td>


                    {
                      getValue(
                        item,
                        [
                          "error_type",
                          "TYPE",
                          "loai_loi"
                        ]
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