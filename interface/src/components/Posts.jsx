import { useEffect, useState } from "react"


export default function Posts() {
    const [posts, setPosts] = useState([])
    const [isFetching, setIsFetching] = useState(true)
    const [value, setValue] = useState("")

    const fetchPosts = async () => {
        let skip = posts.length
        let limit = 20
        if (value !== "") {
            skip = 0
            limit = 200
        }

        try {
            const resp = await fetch(`http://localhost:8000/api/posts?skip=${skip}&limit=${limit}&like=${value}`)
            const res = await resp.json()
            if (value === "") {
                setPosts([...posts, ...res])
            } else {
                setPosts(res)
            }

        } catch(e) {
            console.log(e)
        }
    }

    const handleScroll = async () => {
        if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight) return
        setIsFetching(true)
    }

    const handleChangeValue = async (val) => {
        if (val.length === 0) {
            setPosts([])
            setIsFetching(true)
        } else if (val.length < 3) {
            setValue(val)
            return
        }

        setValue(val)
    }

    useEffect(() => {
        window.addEventListener("scroll", handleScroll)
        return () => window.removeEventListener("scroll", handleScroll)
    }, [])

    useEffect(() => {
        if (!isFetching) return
        fetchPosts()
        setIsFetching(false)
    }, [isFetching])

    useEffect(() => {
        if (value.length > 0 && value.length < 3 || isFetching) return
        fetchPosts()
    }, [value])

    return (
        <div id="posts" className="md:flex justify-center">
            <div className="lg:w-1/2 md:m-10">
                <div className="mt-10 px-5">
                    <input type="text" value={value} onChange={({target}) => handleChangeValue(target.value)}
                        placeholder="search..."
                        className="w-full p-3 rounded-lg outline-0 "
                        />
                </div>
                <div className="my-5 px-5">
                    <p className="text-slate-500">found {posts.length} posts</p>
                </div>
                
                <div className="">
                    {posts.map(post => {
                        return (
                            <div key={post.id} className="mt-10 xl:p-10 p-5 bg-white rounded-lg">
                                <div className="flex items-center" onClick={() => window.open("https://t.me/"+post.username)}>
                                    <img src={"http://localhost:8000/api/photos/"+post.channel_id} alt="channel photo" width={30}
                                        className="rounded-lg"/>
                                    <div className="mx-3 text-xl font-bold">{post.title}</div>
                                </div>
                                <div className="text-slate-700/50">{post.date.replace("T", " ")}</div>
                                <div className="mt-5" dangerouslySetInnerHTML={
                                    {__html: post.message.replace(/(?:\r\n|\r|\n)/g, "<br/>")}}
                                    >
                                </div>

                            </div>
                        )
                    })}
                    <h2>{isFetching && "loading posts..."}</h2>
                </div>
            </div>
        </div>
    )
}