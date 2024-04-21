// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import "./landingPage.css";
// import { Carousel } from "react-responsive-carousel";
// import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader

// const LandingPage = ({ setUserName }) => {
//   const [name, setName] = useState("");
//   const navigate = useNavigate();

//   const handleNameChange = (event) => {
//     setName(event.target.value);
//   };

//   const handleStartChat = () => {
//     setUserName(name);
//     navigate("/chat");
//   };

//   return (
//     // <div className="landing-page">
//     //   <div className="carousel-container">
//     //     <Carousel
//     //       showArrows={false}
//     //       infiniteLoop={true}
//     //       showThumbs={false}
//     //       showStatus={false}
//     //       autoPlay={true}
//     //       swipeable={true}
//     //       emulateTouch={true}
//     //       interval={3000}
//     //     >
//     //       {/* Add your carousel items here */}
//     //       <div>
//     //         <img
//     //           src="https://cdn.vox-cdn.com/thumbor/Mkr-FR0qpPpeEoohWw5q-Wal52E=/0x0:4000x4000/1820x1213/filters:focal(1680x1680:2320x2320):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/55649931/IM_Photo5.0.jpg"
//     //           alt="Destination 1"
//     //         />
//     //         <p className="text">Destination 1</p>
//     //       </div>
//     //       <div>
//     //         <img
//     //           src="https://cdn.vox-cdn.com/thumbor/_6jXI4tJtb0BUY6KRgaRnHc8gyo=/0x0:1000x451/1720x0/filters:focal(0x0:1000x451):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/8829177/AGCuesta.jpg"
//     //           alt="Destination 2"
//     //         />
//     //         <p className="text">Destination 2</p>
//     //       </div>
//     //       <div>
//     //         <img
//     //           src="https://cdn.vox-cdn.com/thumbor/Mkr-FR0qpPpeEoohWw5q-Wal52E=/0x0:4000x4000/1820x1213/filters:focal(1680x1680:2320x2320):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/55649931/IM_Photo5.0.jpg"
//     //           alt="Destination 1"
//     //         />
//     //         <p className="text">Destination 3</p>
//     //       </div>
//     //       <div>
//     //         <img
//     //           src="https://cdn.vox-cdn.com/thumbor/_6jXI4tJtb0BUY6KRgaRnHc8gyo=/0x0:1000x451/1720x0/filters:focal(0x0:1000x451):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/8829177/AGCuesta.jpg"
//     //           alt="Destination 2"
//     //         />
//     //         <p className="text">Destination 4</p>
//     //       </div>
//     //       {/* ... more items */}
//     //     </Carousel>
//     //   </div>

//     //   <div className="input-group">
//     //     <input
//     //       type="text"
//     //       placeholder="Enter Your Name"
//     //       value={name}
//     //       onChange={handleNameChange}
//     //     />
//     //     <button onClick={handleStartChat}>Start Planning Your Trip!</button>
//     //   </div>
//     //   <div className="footer">Help us grow</div>
//     // </div>
//     <div>
//       <div className="background-image"></div>
//       <div className="landing-page">
//         <div className="input-group">
//           <input
//             type="text"
//             placeholder="Enter Your Name"
//             value={name}
//             onChange={handleNameChange}
//           />
//           <button onClick={handleStartChat}>Start Planning Your Trip!</button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default LandingPage;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./landingPage.css"; // Make sure to create this CSS file

const LandingPage = ({ setUserName }) => {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleStartChat = () => {
    setUserName(name);
    navigate("/chat");
  };

  return (
    <div className="landing-container">
      <div className="background-image"></div>
      <div className="cta-content">
        <p className="cta-pretitle">DISCOVER NEW DESTINATIONS</p>
        <h1 className="cta-title">Take a break, Use Trippy</h1>
        <p className="cta-description">
          Plan your dream trip with ease. Unique experiences and tailored
          adventures await, no extensive planning required.
        </p>
        <div className="cta-input-button">
          <input
            type="text"
            placeholder="Enter Your Email"
            value={name}
            onChange={handleNameChange}
          />
          <button className="cta-button" onClick={handleStartChat}>
            Plan your trip now!
          </button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
