import {  useState,useEffect } from "react";
import "./App.css";

function App() {

  const [url, setUrl] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [mediaType, setMediaType] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("")
  const [MultipostP, setMultipostP] = useState([])
  const [MultipostD, setMultipostD] = useState([])
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [coldStart, setColdStart] = useState(false);
  const [factIndex, setFactIndex] = useState(0);
  const [quality, setQuality] = useState("best");
  const [videoTitle, setVideoTitle] = useState("");
  const [videoResolution, setVideoResolution] = useState("");

  //for keyboard moments
    useEffect(() => {
  const handleKeyDown = (e) => {
    if (selectedIndex === null) return;

    if (e.key === "ArrowRight") {
      setSelectedIndex((prev) =>
        prev === MultipostP.length - 1 ? 0 : prev + 1
      );
    }

    if (e.key === "ArrowLeft") {
      setSelectedIndex((prev) =>
        prev === 0 ? MultipostP.length - 1 : prev - 1
      );
    }

    if (e.key === "Escape") {
      setSelectedIndex(null);
    }
  };
  window.addEventListener("keydown", handleKeyDown);
  return () => {
    window.removeEventListener("keydown", handleKeyDown);
  };
}, [selectedIndex, MultipostP.length]);

//for facts
const facts = [
  "Honey never spoils 🍯",
  "Octopuses have three hearts 🐙",
  "Bananas are technically berries 🍌",
  "Sharks existed before trees 🦈",
  "A day on Venus is longer than a year there 🪐",
  "Wombat poop is cube-shaped 😭",
  "The Eiffel Tower grows in summer ☀️",
  "Your brain is more active while dreaming 💭",
  "There are more stars than grains of sand ✨",
  "Cows have best friends 🐄",
  "The moon slowly moves away from Earth 🌕",
  "Sloths can hold their breath longer than dolphins 🦥",
  "Water can boil and freeze at the same time ❄️",
  "Koalas sleep up to 22 hours a day 😴",
  "An apple floats because it’s 25% air 🍎",
  "Some turtles can breathe through their butts 🐢",
  "A cloud can weigh over a million pounds ☁️",
  "The human nose can detect over 1 trillion smells 👃",
  "Sea otters hold hands while sleeping 🦦",
  "There’s enough DNA in your body to stretch to the sun and back ☀️",
  "Flamingos are born grey 🦩",
  "A group of crows is called a murder 🐦",
  "The first alarm clock only rang at 4 AM ⏰",
  "Penguins propose with pebbles 🐧",
  "Some cats are allergic to humans 😭",
  "The heart of a shrimp is in its head 🍤",
  "There are more fake flamingos than real ones in the world 🦩",
  "Butterflies can taste with their feet 🦋",
  "A strawberry isn’t technically a berry 🍓",
  "The shortest war in history lasted 38 minutes ⚔️"
]

useEffect(() => {

  if (!loading) return;

  const interval = setInterval(() => {
    setFactIndex((prev) => (prev + 1) % facts.length)
  }, 4000)

  return () => clearInterval(interval)

}, [loading,facts.length])

  async function handleFetch() {
    setMediaUrl("");
    setMediaType("");
    setDownloadUrl("");
    setMultipostP([]);
    setMultipostD([]);
    setVideoTitle("");
    setVideoResolution("");

     if (!url) {
    alert("Please enter URL");
    return;
    }

    
    try {
      setError("");
      setLoading(true);
      setColdStart(false);
      const coldTimer = setTimeout(() => {
        setColdStart(true)
      }, 12000)
    const response = await fetch(
      `${process.env.REACT_APP_API_URL}/fetch`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url, quality })
      }
    );
    
    const data = await response.json();
    if (!response.ok) {
      setError(data.message);
      setLoading(false)
      setColdStart(false)
      clearTimeout(coldTimer)
      return;
    }
    setLoading(false);
    setColdStart(false)
    clearTimeout(coldTimer)

    const type = data["type"];
    setMediaType(type);
    if (data.title) setVideoTitle(data.title);
    if (data.resolution) setVideoResolution(data.resolution);

    if (type === "Posts") {
      setMultipostP(data["preview_urls"])
      setMultipostD(data["download_urls"])
    }
    else{
      setMediaUrl(data["preview_url"]);
      setDownloadUrl(data["download_url"]);

    }
    

  } catch (error) {
    setError("Something went wrong");
    setLoading(false);
    setColdStart(false)
    console.log("Error:", error);

  }


}

return (
  <div
    style={{
      minHeight: "100vh",
      background: "linear-gradient(to bottom, #1a1a1a, #0f0f0f)",
      color: "white",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      fontFamily: "Arial",
      padding: "20px",
      boxSizing: "border-box",
    }}
  >
    <div
      style={{
        backgroundColor: "#1e1e1e",
        padding: "25px",
        borderRadius: "20px",
        width: "90%",
        maxWidth: "350px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "15px",
        boxShadow: "0 0 20px rgba(0,0,0,0.4)",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontSize: "28px",
          textAlign: "center",
        }}
      >
        📥 Universal Downloader
      </h1>


      <p
        style={{
          marginTop: "-5px",
          color: "#aaaaaa",
          fontSize: "14px",
          textAlign: "center",
        }}
      >
        Download any videos or posts instantly from any platform
      </p>

      <input
        type="text"
        placeholder="Paste Any URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "10px",
          border: "none",
          outline: "none",
          fontSize: "14px",
          boxSizing: "border-box",
        }}
      />

      <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: "6px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <label style={{ fontSize: "12px", color: "#aaa" }}>
            Select Quality:
          </label>
          <span style={{ fontSize: "11px", color: "#00bfff", fontWeight: "bold" }}>
            Up to 4K / 1080p+
          </span>
        </div>
        <select
          value={quality}
          onChange={(e) => setQuality(e.target.value)}
          style={{
            width: "100%",
            padding: "11px 12px",
            borderRadius: "10px",
            border: "1px solid #333",
            backgroundColor: "#282828",
            color: "white",
            fontSize: "14px",
            outline: "none",
            cursor: "pointer",
            boxSizing: "border-box",
          }}
        >
          <option value="best">🌟 Best Available (1080p / 2K / 4K+)</option>
          <option value="2160">🎬 4K Ultra HD (2160p)</option>
          <option value="1440">📺 2K Quad HD (1440p)</option>
          <option value="1080">✨ 1080p Full HD</option>
          <option value="720">📱 720p HD</option>
          <option value="480">💾 480p SD</option>
          <option value="360">⚡ 360p (Data Saver)</option>
          <option value="audio">🎵 Audio Only (MP3)</option>
        </select>
      </div>

      <button
        onClick={handleFetch}
        disabled={loading}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "10px",
          border: "none",
          backgroundColor: "#0095f6",
          color: "white",
          fontWeight: "bold",
          fontSize: "15px",
          transition: "0.2s",
          opacity: loading ? 0.7 : 1,
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        Fetch
      </button>

{loading && (
  <div
    style={{
      width: "100%",
      backgroundColor: "#181818",
      padding: "20px",
      borderRadius: "15px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "15px",
      boxSizing: "border-box",
    }}
  >

    <div className="spinner"></div>

    {!coldStart ? (
      <>
        <h3 style={{ margin: 0 }}>
          Fetching Media...
        </h3>
       
        <p
          style={{
            margin: 0,
            color: "#999",
            textAlign: "center",
            fontSize: "14px",
          }}
        >
          Preparing media for preview and download
        </p>
         <p
  style={{
    margin: 0,
    color: "#00bfff",
    fontSize: "13px",
    textAlign: "center",
    fontStyle: "italic",
  }}
>
  💡 Did you know? {facts[factIndex]}
</p>
      </>
    ) : (
      <>
        <h3
          style={{
            margin: 0,
            textAlign: "center",
          }}
        >
          Starting cloud server...
        </h3>

        <p
          style={{
            margin: 0,
            color: "#999",
            textAlign: "center",
            fontSize: "14px",
            lineHeight: "1.6",
          }}
        >
          Free servers sleep after inactivity.
          <br />
          First request may take 30-60 seconds.
          <br />
        </p>
        
         <p
  style={{
    margin: 0,
    color: "#00bfff",
    fontSize: "13px",
    textAlign: "center",
    fontStyle: "italic",
  }}
>
  💡 Did you know? {facts[factIndex]}
</p>
      </>
    )}

  </div>
)}

      {error && (
        <p
          style={{
            color: "#ff4d4d",
            margin: 0,
            textAlign: "center",
          }}
        >
          {error}
        </p>
      )}

      {mediaType === "Video" && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "12px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          {videoTitle && (
            <p
              style={{
                margin: 0,
                fontSize: "13px",
                fontWeight: "bold",
                color: "#e0e0e0",
                textAlign: "center",
                lineHeight: "1.3",
                wordBreak: "break-word",
              }}
            >
              {videoTitle}
            </p>
          )}

          {videoResolution && (
            <span
              style={{
                fontSize: "11px",
                padding: "3px 8px",
                borderRadius: "6px",
                backgroundColor: "#0095f6",
                color: "white",
                fontWeight: "bold",
              }}
            >
              Quality: {videoResolution}
            </span>
          )}

          <video
            controls
            playsInline
            width="100%"
            style={{
              borderRadius: "12px",
            }}
          >
            <source src={mediaUrl} type="video/mp4" />
          </video>

          <a
            href={downloadUrl}
            download
            style={{
              width: "100%",
            }}
          >
            <button
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                backgroundColor: "#2ea44f",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Download Video {videoResolution ? `(${videoResolution})` : ""}
            </button>
          </a>
        </div>
      )}

      {mediaType === "Audio" && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "12px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          {videoTitle && (
            <p
              style={{
                margin: 0,
                fontSize: "13px",
                fontWeight: "bold",
                color: "#e0e0e0",
                textAlign: "center",
                lineHeight: "1.3",
              }}
            >
              {videoTitle}
            </p>
          )}

          <span
            style={{
              fontSize: "11px",
              padding: "3px 8px",
              borderRadius: "6px",
              backgroundColor: "#9333ea",
              color: "white",
              fontWeight: "bold",
            }}
          >
            Audio (MP3)
          </span>

          <audio
            controls
            style={{
              width: "100%",
              marginTop: "5px",
            }}
          >
            <source src={mediaUrl} type="audio/mpeg" />
          </audio>

          <a
            href={downloadUrl}
            download
            style={{
              width: "100%",
            }}
          >
            <button
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                backgroundColor: "#2ea44f",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Download Audio (MP3)
            </button>
          </a>
        </div>
      )}
      {mediaType === "Posts" && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "10px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          {MultipostP.map((MultipostP, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "8px",
              }}
            >
              <img
                src={MultipostP}
                alt={`post-${index}`}
                onClick={() => setSelectedIndex(index)}
                style={{
                  width: "100%",
                  borderRadius: "12px",
                  objectFit: "cover",
                  cursor: "pointer",
                }}
              />

              <a
                href={MultipostD[index]}
                download
                style={{
                  width: "100%",
                }}
              >
                <button
                  style={{
                    width: "100%",
                    padding: "8px",
                    borderRadius: "10px",
                    border: "none",
                    backgroundColor: "#2ea44f",
                    color: "white",
                    fontWeight: "bold",
                    cursor: "pointer",
                  }}
                >
                  Download
                </button>
              </a>
            </div>
          ))}
        </div>
      )}
      {mediaType === "Post" && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "10px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          <img
            src={mediaUrl}
            alt="Instagram Post"
            width="100%"
            style={{
              borderRadius: "12px",
            }}
          />

          <a
            href={downloadUrl}
            download
            style={{
              width: "100%",
            }}
          >
            <button
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                backgroundColor: "#2ea44f",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Download Post
            </button>
          </a>
        </div>
      )}
      {selectedIndex !== null && (
  <div
    style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100vw",
      height: "100vh",
      backgroundColor: "rgba(0,0,0,0.9)",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 9999,
    }}
  >
    <button
      onClick={() => setSelectedIndex(null)}
      style={{
        position: "absolute",
        top: "20px",
        right: "20px",
        fontSize: "30px",
        background: "none",
        color: "white",
        border: "none",
        cursor: "pointer",
      }}
    >
      ✕
    </button>
      <div
  style={{
    position: "absolute",
    top: "20px",
    left: "50%",
    transform: "translateX(-50%)",
    color: "white",
    fontSize: "18px",
    fontWeight: "bold",
  }}
>
  {selectedIndex + 1} / {MultipostP.length}
</div>
    <button
      onClick={() =>
        setSelectedIndex((prev) =>
          prev === 0 ? MultipostP.length - 1 : prev - 1
        )
      }
      style={{
        position: "absolute",
        left: "20px",
        fontSize: "40px",
        background: "none",
        color: "white",
        border: "none",
        cursor: "pointer",
      }}
    >
      ‹
    </button>

    <img
      src={MultipostP[selectedIndex]}
      alt=""
      style={{
        maxWidth: "90%",
        maxHeight: "90%",
        borderRadius: "12px",
      }}
    />
    <a
  href={MultipostD[selectedIndex]}
  download
  style={{
    position: "absolute",
    bottom: "20px",
    textDecoration: "none",
  }}
>
  <button
    style={{
      padding: "12px 20px",
      borderRadius: "12px",
      border: "none",
      backgroundColor: "#2ea44f",
      color: "white",
      fontWeight: "bold",
      cursor: "pointer",
      fontSize: "16px",
    }}
  >
    Download
  </button>
</a>

    <button
      onClick={() =>
        setSelectedIndex((prev) =>
          prev === MultipostP.length - 1 ? 0 : prev + 1
        )
      }
      style={{
        position: "absolute",
        right: "20px",
        fontSize: "40px",
        background: "none",
        color: "white",
        border: "none",
        cursor: "pointer",
      }}
    >
      ›
    </button>
  </div>
)}
      <p
        style={{
          fontSize: "12px",
          color: "#777",
          marginTop: "5px",
          textAlign: "center",
        }}
      >
        ⚠️ YouTube videos feature is experimental / may fail due to platform restrictions
      </p>
    </div>
  </div>
);
}

export default App;