import React, { useState } from "react";


const FileUpload = () => {
    const [selectedfile, setSelectedfile] = useState();
    const [isseleted, setIsselected] = useState(false);
    console.log(selectedfile)

    const handleChange = (event) => {
        setSelectedfile(event.target.files[0]);
        setIsselected(true);
    };

    const handleUpload = async () => {
        console.log("ENTER KEY")


        // if (isseleted===true) alert("uploaded")
        // else alert("!!! Please Select file")
        try {
            const res = await fetch("http://localhost/fileupload",
                {
                    method: "Post",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: JSON.stringify({ selectedfile })
                });
                const response = await res.json()
                console.log(response)
        }
        catch (error) {
            console.error('Error fetching data:', error);
        }

        
    }

    return (
        <>
            <input type="file" onChange={handleChange} />
            {isseleted ? (<p>{selectedfile.name}</p>) : (<p>Not selected!!!</p>)}
            <button onClick={handleUpload}>Upload</button>

        </>
    );
}

export default FileUpload;