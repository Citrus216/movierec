const RecommendationScore = ({ recScore, simScore }) => {

    const getColor = (score) => {
        if (score > 66) {
            return "#3ec15f";
        } else if (score > 33) {
            return "#e9d416";
        } else {
            return "#d42b2f";
        }
    }

    const style = {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        height: '200px',
        width: '200px',
        backgroundColor: '#fff',
        borderRadius: '20%',
        border: '1px solid #000',
        fontSize: '24px',
        fontWeight: 'bold',
        marginRight: '20px',
    };

    return (
        <div style={{display: "flex", flexDirection: "column", justifyContent: "center"}}>
            <div style={{ display: "flex", flexDirection: "row" }}>
                <div style={style}>
                    <p></p>
                    <p style={{fontSize:"48pt", margin: "24px", color: getColor(recScore)}}>{recScore}</p>
                    <p style={{fontSize:"12pt"}}>Recommendation</p>
                </div>
                <div style={style}>
                    <p></p>
                    <p style={{fontSize:"48pt", margin: "24px", color: getColor(simScore)}}>{simScore}</p>
                    <p style={{fontSize:"12pt"}}>Similarity</p>
                </div>
            </div>
        </div>
    );
};

export default RecommendationScore;