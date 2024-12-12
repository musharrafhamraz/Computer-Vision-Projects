// import './Styles.css';
// import React, { useEffect, useRef } from 'react';
// 
// const VideoStream = () => {
//   const videoRef = useRef();
//   const mediaSourceRef = useRef();

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await fetch('http://localhost:5000/api/video_feed_cam1');
//         const reader = response.body.getReader();
//         const video = videoRef.current;

//         const mediaSource = new MediaSource();
//         mediaSourceRef.current = mediaSource;

//         video.src = URL.createObjectURL(mediaSource);

//         mediaSource.addEventListener('sourceopen', async () => {
//           const sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');

//           const cleanup = () => {
//             mediaSource.endOfStream();
//             mediaSource.removeEventListener('sourceopen', cleanup);
//             URL.revokeObjectURL(video.src);
//           };

//           while (true) {
//             const { done, value } = await reader.read();

//             if (done) {
//               cleanup();
//               break;
//             }

//             const blob = new Blob([value], { type: 'image/jpeg' });
//             const arrayBuffer = await blob.arrayBuffer();

//             if (!sourceBuffer.updating) {
//               sourceBuffer.appendBuffer(arrayBuffer);
//             }

//             // Adjust the delay for the desired frame rate (approximately 30 fps)
//             await new Promise(resolve => setTimeout(resolve, 33));
//           }
//         });

//         // Handle errors and clean up if necessary
//         mediaSource.addEventListener('error', () => {
//           console.error('MediaSource error');
//           mediaSourceRef.current = null; // Reset the reference
//         });

//         // Adjust the delay for the desired frame rate (approximately 30 fps)
//         await new Promise(resolve => setTimeout(resolve, 33));
//       } catch (error) {
//         console.error('Error fetching data:', error);
//       }
//     };

//     fetchData();

//     return () => {
//       // Cleanup function
//       const mediaSource = mediaSourceRef.current;
//       if (mediaSource) {
//         mediaSource.endOfStream();
//         URL.revokeObjectURL(videoRef.current.src);
//       }
//     };
//   }, []);

//   return (
//     <div className='VideoStream'>
//       <div className='VideoTop'>
//         <h2>VideoStream</h2>
//         <h5>See all</h5>
//       </div>
//       <div className='Videos'>
//         <video ref={videoRef} width='640' height='280' controls autoPlay />
//       </div>
//     </div>
//   );
// };

// export default VideoStream;
import React, { useEffect, useRef } from 'react';

const VideoStream = () => {
  const videoRef = useRef();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/video_feed_cam1');
        const videoStreamUrl = response.url;

        // Set the video element's src attribute directly
        videoRef.current.src = videoStreamUrl;

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();

  }, []);

  return (
    <div className='VideoStream'>
      <div className='VideoTop'>
        <h2>VideoStream</h2>
        <h5>See all</h5>
      </div>
      <div className='Videos'>
        {/* <video ref={videoRef} width='100%' height='auto' controls autoPlay /> */}
        <img src="http://localhost:5000/api/video_feed_cam1"  width='640px' height='300px' alt="" />
        
      </div>
    </div>
  );
};

export default VideoStream;
