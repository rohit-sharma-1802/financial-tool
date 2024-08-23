import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onResult }) => {
    const [file, setFile] = useState(null);

    const onFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const onFileUpload = () => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const data = JSON.parse(e.target.result);
            axios.post('http://localhost:5000/upload', data)
                .then((response) => {
                    onResult(response.data);
                })
                .catch((error) => {
                    console.error('There was an error!', error);
                });
        };
        reader.readAsText(file);
    };

    return (
        <div>
            <input type="file" onChange={onFileChange} />
            <button onClick={onFileUpload}>Upload</button>
        </div>
    );
};

export default FileUpload;
