import React, {FC, useState, useEffect} from 'react';
import axios from 'axios';

const NewVinyl: FC = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [vinyls, setVinyls] = useState([])
    const baseUrl = "https://smartstore.naver.com/i/v1/stores/"
    const baseUrlData = "/pc-widgets/whole-products?sort=RECENT"
    const data : {
        name: string,
        site: string
    }[] = [
        {
            name: "SeoulVinyl",
            site: "https://smartstore.naver.com/i/v1/stores/100129192/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
        },
        // {
        //     name: "RecordStock",
        //     site: "100804461",
        // }
    ]

    useEffect(() => {
        const getNewVinyl = async (site: string) => {
            const response = await axios.get(site, {});
            console.log(response);
        }
        data.forEach((dataUnit:{name: string, site:string}) => {
            var url: string;
            if (dataUnit.site.startsWith("http")) {
                url = dataUnit.site
            } else {
                url = baseUrl + dataUnit.site + baseUrlData
            }
        })
        getNewVinyl("https://smartstore.naver.com/i/v1/stores/100129192/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40")

    }, [])

    return (
        <div>
            new vinyls
        </div>
    )
}

export default NewVinyl;