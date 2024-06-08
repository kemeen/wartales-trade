import pathlib
from wartales_trade.location import Location
from wartales_trade.trade_good import TradeGood
import yaml
from functools import partial

LOCATIONS = pathlib.Path("locations.yaml")
TRADE_GOODS = pathlib.Path("trade_goods.yaml")

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# root = tk.Tk()

# b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
# b1.pack(side=LEFT, padx=5, pady=10)

# b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE))
# b2.pack(side=LEFT, padx=5, pady=10)

# root.mainloop()


def load_trade_goods(path: pathlib.Path) -> dict[str, TradeGood]:
    with TRADE_GOODS.open("r", encoding="utf-8") as f:
        _trade_goods = yaml.safe_load(f)

    trade_goods = {
        name: TradeGood(name=name, base_price=price)
        for name, price in _trade_goods.items()
    }
    return trade_goods


def load_locations(
    path: pathlib.Path, trade_goods: dict[str, TradeGood]
) -> dict[str, Location]:
    with LOCATIONS.open("r", encoding="utf-8") as f:
        _locations = yaml.safe_load(f)

    locations = dict()
    for name, location_data in _locations.items():
        location_trade_goods = [
            trade_goods.get(name) for name in location_data.get("Trade Goods")
        ]
        location_buy_prices = [
            (trade_goods.get(name), price)
            for name, price in location_data.get("buying").items()
        ]
        locations[name] = Location(
            name=name, trade_goods=location_trade_goods, buying=location_buy_prices
        )
    return locations


def clear_frame(target_frame):
    # destroy all widgets from frame
    # print("DESTROY")
    for w in target_frame.winfo_children():
        w.destroy()
        # print("DESTROY TARGET")


def set_trade_location(e: tk.Event, locations: dict[str, Location]) -> None:
    # print("set trade locations")
    clear_frame(trade_view_frame)

    location_name = e.widget.get()
    for loc in sorted(locations.values(), key=lambda x: x.name):
        if loc.name == location_name:
            continue
        location_profit_view = LocationProfit(
            trade_view_frame,
            origin=locations[location_name],
            target=loc,
            bootstyle="default",
        )
        location_profit_view.pack(side=TOP, pady=20, padx=10, fill="x")


class LocationProfit(ttk.Labelframe):
    def __init__(
        self, master, origin: Location, target: Location, bootstyle: str, **kwargs
    ):
        super().__init__(master, text=target.name, bootstyle=bootstyle, **kwargs)

        for tg in sorted(origin.trade_goods, key=lambda x: x.name):
            price = target.get_price_for_trade_good(tg)
            if price is None:
                continue
            tg_frame = ttk.Frame(self, bootstyle=bootstyle)
            tg_name_label = ttk.Label(tg_frame, text=tg.name, bootstyle="default")
            tg_price_label = ttk.Label(tg_frame, text=f"{price}g", bootstyle="default")
            tg_profit_label = ttk.Label(
                tg_frame, text=f"{price-tg.base_price}g", bootstyle="default"
            )
            tg_percent_label = ttk.Label(
                tg_frame,
                text=f"{(price-tg.base_price)/tg.base_price:.2%}",
                bootstyle="default",
            )
            tg_name_label.pack(side=LEFT, fill="x", expand=True)
            tg_price_label.pack(side=LEFT, padx=20)
            tg_profit_label.pack(side=LEFT, padx=20)
            tg_percent_label.pack(side=LEFT, padx=20)
            tg_frame.pack(fill="x", expand=False)


trade_goods = load_trade_goods(TRADE_GOODS)
locations = load_locations(path=LOCATIONS, trade_goods=trade_goods)
# for loc in locations:
#     print(loc)
location_names = sorted(locations.keys())
root = ttk.Window(themename="darkly", title="Wartales Trade Helper", size=(400, 300))

# Tkinter Variables
current_location = tk.StringVar()

# create a new notebook
nb = ttk.Notebook(root, bootstyle="dark")
nb.pack(pady=20, padx=20, fill="both", expand=True)

# create frames
tab1 = ttk.Frame(nb)
tab2 = ttk.Frame(nb)
tab3 = ttk.Frame(nb)

tab1.pack(fill="both", expand=True)
tab2.pack(fill="both", expand=True)
tab3.pack(fill="both", expand=True)

# set the frame as a tab in the notebook
nb.add(tab1, text="Trade")
nb.add(tab2, text="Trade Goods")
nb.add(tab3, text="Locations")

# Trade Tab
tab1_label = ttk.Label(tab1, text="Trade Overview")
tab1_label.pack(side=TOP)

# Left Trade Frame
left_trade_frame = ttk.Frame(tab1, bootstyle="light")
location_label = ttk.Label(left_trade_frame, text="Location", bootstyle="inverse-light")
location_selection = ttk.Combobox(
    left_trade_frame,
    values=location_names,
    bootstyle="light",
    textvariable=current_location,
)
location_selection.set(location_names[0])
location_selection.bind(
    "<<ComboboxSelected>>", partial(set_trade_location, locations=locations)
)

location_label.pack(side=TOP)
location_selection.pack(side=TOP)

left_trade_frame.pack(side=LEFT, padx=10, pady=10, fill="y", expand=False)

# right trade frame
right_trade_frame = ttk.Frame(tab1, bootstyle="light")
label_frame = ttk.Frame(right_trade_frame, bootstyle="default")
trade_view_frame = ttk.Frame(right_trade_frame, bootstyle="default")
label_frame.pack(side=TOP)
trade_view_frame.pack(side=TOP, fill="x", expand=True)
location_label_static = ttk.Label(label_frame, text="Current Location: ")
current_location_label = ttk.Label(
    label_frame,
    bootstyle="light",
    text="",
    textvariable=current_location,
)

location_label_static.pack(side=LEFT)
current_location_label.pack(side=LEFT)

# trade_location_frames = dict()
# for loc in sorted(locations.values(), key=lambda x: x.name):
#     if loc.name == current_location.get():
#         continue

#     buying_frame = ttk.Labelframe(right_trade_frame, bootstyle="default", text=loc.name)
#     ttk.Labelframe(right_trade_frame, bootstyle="default", text=loc.name)
#     for tg, price in loc.buying:
#         tg_frame = ttk.Frame(buying_frame, bootstyle="default")
#         tg_name_label = ttk.Label(tg_frame, text=tg.name, bootstyle="default")
#         tg_price_label = ttk.Label(tg_frame, text=f"{price}g", bootstyle="default")
#         tg_name_label.pack(side=LEFT, fill="x", expand=True)
#         tg_price_label.pack(side=RIGHT)
#         tg_frame.pack(fill="x", expand=False)
#     buying_frame.pack(side=TOP, fill="x", expand=True, padx=20, pady=10)

right_trade_frame.pack(side=LEFT, padx=10, pady=10, fill="both", expand=True)

# Trade Goods Tab
tab2_label = ttk.Label(tab2, text="Manage Trade Goods")
tab2_label.pack(side=TOP, pady=5)

for tg in sorted(trade_goods.values(), key=lambda x: x.name):
    tg_frame = ttk.Labelframe(tab2, bootstyle="default", text=tg.name)
    tg_name_label = ttk.Label(tg_frame, text=tg.name)
    tg_price_label = ttk.Label(tg_frame, text=f"{tg.base_price}g", bootstyle="default")
    tg_name_label.pack(side=LEFT, fill="both", expand=True)
    tg_price_label.pack(side=RIGHT)
    tg_frame.pack(fill="x", expand=False, padx=10, pady=5)

# Locations Tab
tab3_label = ttk.Label(tab3, text="Manage Locations")
tab3_label.pack(side=TOP)

for loc in sorted(locations.values(), key=lambda x: x.name):
    loc_frame = ttk.Labelframe(tab3, bootstyle="default", text=loc.name)

    # selling
    selling_frame = ttk.Labelframe(loc_frame, bootstyle="default", text="Selling")
    for tg in loc.trade_goods:
        tg_frame = ttk.Frame(selling_frame, bootstyle="default")
        tg_name_label = ttk.Label(tg_frame, text=tg.name, bootstyle="default")
        tg_price_label = ttk.Label(
            tg_frame, text=f"{tg.base_price}g", bootstyle="default"
        )
        tg_name_label.pack(side=LEFT, fill="x", expand=True)
        tg_price_label.pack(side=RIGHT)
        tg_frame.pack(fill="x", expand=False)
    selling_frame.pack(side=LEFT, fill="x", expand=True, padx=20, pady=10)

    # buying
    buying_frame = ttk.Labelframe(loc_frame, bootstyle="default", text="Buying")
    for tg, price in loc.buying:
        tg_frame = ttk.Frame(buying_frame, bootstyle="default")
        tg_name_label = ttk.Label(tg_frame, text=tg.name, bootstyle="default")
        tg_price_label = ttk.Label(tg_frame, text=f"{price}g", bootstyle="default")
        tg_name_label.pack(side=LEFT, fill="x", expand=True)
        tg_price_label.pack(side=RIGHT)
        tg_frame.pack(fill="x", expand=False)
    buying_frame.pack(side=LEFT, fill="x", expand=True, padx=20, pady=10)
    loc_frame.pack(fill="x", expand=False, padx=5, pady=10)

root.mainloop()
