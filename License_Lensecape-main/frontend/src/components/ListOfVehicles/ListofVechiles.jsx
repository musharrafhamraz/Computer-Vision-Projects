import "./style.css";
import Datapicker from "./Datapicker";
import ListTable from "./ListTable";
const ListofVechiles = () => {
  return (
    <div className='ListOfVechile'>
      <nav className='Nav-List'>
        <h2>List of Vehicles</h2>
        <input type='text' placeholder='Search for anything...' id='Search' />
        <div>
          <Datapicker />
        </div>
        <div type='Download' id='Download' className='Downloadbtn'>
          <svg
            xmlns='http://www.w3.org/2000/svg'
            width='14'
            height='16'
            viewBox='0 0 14 16'
            fill='none'>
            <path
              d='M7 1.25V12.75M7 12.75L2 8.25M7 12.75L11.5 8.25M1 14.75H13'
              stroke='white'
              strokeLinecap='round'
            />
          </svg>{" "}
          <span></span> Download
        </div>
        <div>
          <span>See ALL</span>
        </div>
      </nav>

      <ListTable />
    </div>
  );
};

export default ListofVechiles;
