import asyncio


def get_loop():
    return (True,
            asyncio.get_event_loop(),
            id(asyncio.get_event_loop())
            )


async def async_main():
    print(get_loop())


def main():
    print(get_loop())


if __name__ == '__main__':
    # no loop
    main()
    # running loop
    asyncio.run(async_main())
    # stopped loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()

# (True, <_UnixSelectorEventLoop running=False closed=False debug=False>, 140062513829776)
# (True, <_UnixSelectorEventLoop running=True closed=False debug=False>, 140062508314464)
# (True, <_UnixSelectorEventLoop running=False closed=False debug=False>, 140062508507376)
