// // DataTable.js

// DataTable.js
import React, { useState, useEffect } from "react";
import { useTable } from "react-table";

const DataTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/get_excel_data");
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const columns = React.useMemo(
    () => [
      {
        Header: "Timestamp",
        accessor: "Timestamp",
      },
      {
        Header: "Plate Number",
        accessor: "Plate Number",
      },
      {
        Header: "Class ID",
        accessor: "Class ID",
      },
      {
        Header: "Confidence",
        accessor: "Confidence",
      },
    ],
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <table {...getTableProps()} style={{ borderCollapse: "collapse", width: "100%" }}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr key={headerGroup.id} {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th key={column.id} {...column.getHeaderProps()} style={{ borderBottom: "2px solid #ddd", padding: "8px", textAlign: "left" }}>
                {column.render("Header")}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row) => {
          prepareRow(row);
          return (
            <tr key={row.id} {...row.getRowProps()} style={{ borderBottom: "1px solid #ddd" }}>
              {row.cells.map((cell) => (
                <td key={cell.row.id} {...cell.getCellProps()} style={{ padding: "8px", textAlign: "left" }}>
                  {cell.render("Cell")}
                </td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default DataTable;





// import React from "react";
// import { useTable } from "react-table";
// import packageJson from "./package.json";

// const DataTable = () => {
//   // Extract data from package.json
//   const data = packageJson.tableData; // Assume you have a "tableData" field in your package.json
//   // const data =[ plateNo: "ABC123", modelType: "toyota Gli" , logType: "Entry" ,
//   // date:"2014-12-01T00:00:00", status:"Active"]
//   // Define columns
//   const columns = React.useMemo(
//     () => [
//       {
//         Header: "Plate No",
//         accessor: "plateNo",
//       },
//       {
//         Header: "Model/Vehicle Type",
//         accessor: "modelType",
//       },
//       {
//         Header: "Log Type",
//         accessor: "logType",
//       },
//       {
//         Header: "Date",
//         accessor: "date",
//       },
//       {
//         Header: "Status",
//         accessor: "status",
//       },
//     ],
//     []
//   );

//   // Create a table instance
//   const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
//     useTable({ columns, data });

//   return (
//     <table
//       {...getTableProps()}
//       style={{
//         borderCollapse: "collapse",
//         width: "100%",
//         // display: "flex",
//         flexWrap: "wrap",
//         // gap: "2%",
//         // flexShrink: "10",
//         // borderTop: "10px solid Pink",
//       }}>
//       <thead>
//         {headerGroups.map((headerGroup) => (
//           <tr key={columns.id} {...headerGroup.getHeaderGroupProps()}>
//             {headerGroup.headers.map((column) => (
//               <th
//                 key={columns.id}
//                 {...column.getHeaderProps()}
//                 style={{
//                   borderBottom: "2px solid #ddd",
//                   background: "transparent",
//                   padding: "8px",
//                   textAlign: "left",
//                 }}>
//                 {column.render("Header")}
//               </th>
//             ))}
//           </tr>
//         ))}
//       </thead>
//       <tbody {...getTableBodyProps()}>
//         {rows.map((row) => {
//           prepareRow(row);
//           return (
//             <tr
//               key={row.id}
//               {...row.getRowProps()}
//               style={{ borderBottom: "1px solid #ddd" }}>
//               {row.cells.map((cell) => (
//                 <td
//                   key={row.id}
//                   {...cell.getCellProps()}
//                   style={{
//                     padding: "8px",
//                     textAlign: "left",
//                   }}>
//                   {cell.render("Cell")}
//                 </td>
//               ))}
//             </tr>
//           );
//         })}
//       </tbody>
//     </table>
//   );
// };

// export default DataTable;
