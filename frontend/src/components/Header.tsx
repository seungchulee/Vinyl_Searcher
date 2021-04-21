import React, {FC} from 'react';
import {Link} from 'react-router-dom';
import styled from 'styled-components';

const Wrapper = styled.div`

`;

const Header: FC = () => {
    return (
        <div className="ui secondary pointing menu" style={{border:"0px"}}>
            <div className="ui right aligned grid">
                <div className="center aligned two column row">
                    <div className="column">
                        <div className="ui segment" style={{border:"0px"}}>
                            <Link to="/" className="item">
                                New
                            </Link>
                        </div>
                    </div>
                    <div className="column">
                        <div className="ui segment" style={{border:"0px"}}>
                            <Link to="/search" className="item">
                                Search
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Header;