"""Class: CS230--Section 5
Name: Gabe Holmes
Description: This is a final project that took much time and effort in an attempt to showcase
how a dataset can creatively be used to help any user of such data to learn something new and
be able to interact with the data effectively!
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student."""

import statistics
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
import numpy as np
import math

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Times New Roman', serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def read_meteorite_landings(FILENAME):
    df = pd.read_csv(FILENAME)
    df = df.rename(columns={
        'name': 'Name',
        'id': 'ID',
        'nametype': 'NameType',
        'recclass': 'Class',
        'mass (g)': 'Mass (g)',
        'fall': 'Witnessed',
        'year': 'Year',
        'reclat': 'Lat',
        'reclong': 'Lon'
    })


    df["Lat"] = pd.to_numeric(df["Lat"], errors='coerce')
    df["Lon"] = pd.to_numeric(df["Lon"], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Mass (g)'] = pd.to_numeric(df['Mass (g)'], errors='coerce')
    return df


def normalize_class(x):
    normalized = str(x).upper().strip().replace('/', '-').replace('?', '')
    return normalized


def assign_category(Class):
    broad_categories = {
        'Carbonaceous Chondrites': ['CI', 'CM', 'CR', 'CO', 'CV', 'CK'],  # Carbonaceous chondrites
        'Enstatite Chondrites': ['EH', 'EL'],  # Enstatite chondrites
        'Ordinary Chondrites': ['H', 'L', 'LL', 'OC'],  # Ordinary chondrites
        'Kakangari Chondrites': ['K3'],  # Kakangari chondrites
        'Primitive Achondrites': ['ACAPULCOITE', 'BRACHINITE', 'WINONAITE'],  # Primitive achondrites
        'Achondrites': ['ANGRITE', 'AUBRITE', 'CHASSIGNITE', 'DIOGENITE', 'EUCRITE', 'HOWARDITE', 'NAKHLITE',
                        'UREILITE'],  # Achondrites
        'Stony-Iron': ['MESOSIDERITE', 'PALLASITE', 'CR CL'],  # Stony-iron
        'Iron': ['IRON', 'IA', 'IB', 'IC', 'IIA', 'IIB', 'IIC', 'IID', 'IIIA', 'IIIB', 'IVA', 'IVB']  # Irons
    }
    #[ITERLOOP] - Iterates through a dictionary to return a list of tuples, that is then iterated through to return a category!
    #[DICTMETHOD] - Used .items() here and .keys() below on line 247
    for category, patterns in broad_categories.items():
        for p in patterns:
            if Class.startswith(p) or p in Class:
                return category
    return 'Other'
# Home page
def home_page(page):
    st.image("meteor_shower.png", caption="2011 Perseids Meteor Shower")
    st.title("METEORITE MANIA")
    st.subheader("Welcome! Use the sidebar to navigate to different pages!")

    st.text("")
    st.text("")

    st.header("What are the different types of meteorites?")
    st.header("What size crater would a meteorite cause if it hit the Earth?")
    st.subheader("Look through the sidebar to find out!")

    st.text("")
    st.text("")

    st.header("What is a meteorite?")
    st.subheader("The most basic definition of a meteorite is: A rock that fell to Earth from space. But most meteorites come from asteroids that"
                 " are shattered upon entering our atmosphere. Many asteroids are in the asteroid belt between Mars and Jupiter,"
                 " and Jupiter slings one at us every so often.")
    st.header("Below are the different types of meteorites you will learn about.")
    st.subheader("There are three main types of meteorites.")

    st.text("")
    st.text("")
    st.text("")

    st.image("iron_meteorite2.jpg")
    st.header("Iron Meteorites ")
    st.subheader("Mainly consist of an iron-nickel alloy with a crystalline structure that tends to form bands")

    st.text("")
    st.text("")
    st.text("")


    st.image("stony_iron.jpeg",width=500)
    st.header("Stony-Iron Meteorites")
    st.subheader("A good in-between, made of equal parts iron-nickel metal and silicate minerals. "
             "There are two types.")

    st.image("pallasite.jpg")
    st.subheader("Pallasite")
    st.write("Pallasites are beautiful with their olive-green crystals that form as clusters of gemstones called olivine. It is "
             "thought by some that olivine is formed where the metal core and silicate meet.")

    st.image("mesosiderite.jpg")
    st.subheader("Mesosiderite")
    st.write("Although not as pretty, mesosiderites have a strong historical value. They are the result of collision that happen"
             "between rock fragment that form together from molten metals and compressed fragments of silicate rocks. The same thing "
             "probably happened when many collisions of particles around the sun formed the earliest version of Earth almost 4.6 billion years ago!")

    st.text("")
    st.text("")
    st.text("")

    st.image("stony_meteorite.jpeg", width=700)
    st.header("Stony Meteorites")
    st.subheader("Consist mostly of silicate minerals. There are two main types")

    st.image("chondrite.jpg")
    st.subheader("Chondrites")
    st.write("Their name comes from the Greek 'chondres' meaning sand grains. They too have much historical/scientific value as they are the building "
             "blocks of our solar system.")

    st.image("achondrite.jpg")
    st.subheader("Achondrites")
    st.write("Achondrites are igneous, meaning that at some point magma cooled to create these meteorites. They can tell us much about the internal "
             "structure and formation of the planets, including Earth.")

    st.write("All information and reference photos were received from the following resources:"
             "\nhttps://www.nhm.ac.uk/discover/types-of-meteorites.html"
             "\nhttps://news.uchicago.edu/explainer/formation-earth-and-moon-explained#howwhenearth"
             "\nhttps://www.amnh.org/exhibitions/permanent/meteorites/meteorites/what-is-a-meteorite")

def classification_colors():
    colors = {'Carbonaceous Chondrites': [180, 220, 127],  # Willow Green
              'Enstatite Chondrites': [254, 255, 165],  # Lemon Cream
              'Ordinary Chondrites': [255, 160, 172],  # Cotton Candy
              'Kakangari Chondrites': [255, 107, 107],  # Tangerine
              'Primitive Achondrites': [127, 85, 125],  # Dusty Lavender
              'Achondrites': [247, 23, 53],  # Strawberry Red
              'Stony-Iron': [100, 255, 200],  # Cyan
              'Iron': [165, 127, 96], # Faded Copper
              'Other': [100, 100, 100]
              }
    return colors


# Map Page

def map_page(df):
    st.title("Meteorite Landings")
    #[COLUMNS] - Specify the only columns I desire to be shown
    #[SORT] - Sorted meteorite landings by ID
    sorted_df = df.sort_values(by="ID").reset_index(drop=True)
    st.dataframe(sorted_df[['Name','ID','Mass (g)','Year','Composition','Lat','Lon']])

    """
    By reading online forums on ways to format items and widgets in streamlit, I learned that streamlit doesn't have
    a nuanced, built-in function to dynamically format a website, at least not to the same extent as html. And I wanted
    to create legends for my pie chart and map that were sleek and informtaive. So I watched this tutorial on using html in 
    streamlit and read streamlit community forums. https://www.youtube.com/watch?v=sbv3yK5pMgU&t=480s 
    """
    legend_html = """
    <style>
    .legend-box {
        position: absolute;
        top: 255px;
        right: 5px;
        background: rgba(0,0,0,0.5);
        padding: 12px 18px;
        border-radius: 10px;
        z-index: 9999;
        color: white;
        font-size: 12px;
        line-height: 20px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
    }
    .legend-color {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        margin-right: 8px;
        border: 1px solid white;
    }
    </style>

    <div class="legend-box">
        <div class="legend-item"><div class="legend-color" style="background: rgb(165, 127, 96);"></div>Iron</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(255, 160, 172);"></div>Ordinary Chondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(180, 220, 127);"></div>Carbonaceous Chondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(254, 255, 165);"></div>Enstatite Chondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(255, 107, 107);"></div>Kakangari Chondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(127, 85, 125);"></div>Primitive Achondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(247, 23, 53);"></div>Achondrites</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(100, 255, 200);"></div>Stony-Iron</div>
        <div class="legend-item"><div class="legend-color" style="background: rgb(100, 100, 100);"></div>Other</div>
    </div>
    """
    st.header("Map of Meteorite Landings")
    #[FUNCCALL2] - Called function 'classification_colors' twice in the program. One for each time a legend was used (map and pie chart).
    df['color'] = df['Composition'].map(classification_colors())
    df['color'] = df['color'].apply(lambda x: x if isinstance(x, list) else [0, 0, 0])
    df['radius'] = np.log10(df['Mass (g)']) * 10000
    st.markdown(legend_html, unsafe_allow_html=True)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Lon, Lat]',
        get_radius= 'radius',
        get_fill_color='color',
        pickable=True
    )

    view = pdk.ViewState(
        latitude=df["Lat"].mean(),
        longitude=df["Lon"].mean(),
        zoom=2
    )

    tooltip = {
        "html": "<b>Name:</b> {Name}<br/>"
                "<b>Lat:</b> {Lat}<br/>"
                "<b>Lon:</b> {Lon}<br/>"
                "<b>Class:</b> {Class}<br/>"
                "<b>Mass (g):</b> {Mass (g)}<br/>"
                "<b>Year:</b> {Year}",
        "style": {"backgroundColor": "black", "color": "white"}
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip=tooltip
    )
    #[MAP]
    st.pydeck_chart(r)
    st.write("Larger circles have a larger mass while smaller circles have a smaller mass")



# Tables/Diagrams Page
def diagrams_page(df):
    st.title("Statistics About Meteorites")

    st.subheader("Number of Meteorite Landings by Year")


    #[MAXMIN]
    year_min = int(df['Year'].min())
    year_max = int(df['Year'].max())
    #[ST2]
    selected_year_range = st.slider(
        'Select year range',
        min_value = year_min,
        max_value = year_max,
        value = (year_min, year_max)
    )

    #[FILTER2]
    df_filtered = df[(df['Year'] >= selected_year_range[0]) &
                     (df['Year'] <= selected_year_range[1])]

    counts = df_filtered.groupby('Year').size().sort_index().reset_index(name='Count')
    chart = alt.Chart(counts).mark_bar().encode(
        x='Year:O',
        y='Count:Q',
        color= alt.value("black"),
        ).configure_axis(labelColor='black', gridColor='gray',titleColor='black')
    
    #[CHART1]
    st.altair_chart(chart, use_container_width=True)

    # Meteorite type piechart, type mapping pulled from American Museum of Natural History
    st.subheader("Types of Meteorites Found by Percent")

    def autopct_filter(pct):
        return f'{pct:.1f}%' if pct > 2 else ''


    composition_counts = df['Composition'].value_counts()
    comp_order = composition_counts.index
    # [FUNCCALL2] - Called function 'classification_colors' twice in the program. One for each time a legend was used (map and pie chart).
    colors_dict = classification_colors()
    pie_colors = [np.array(colors_dict[c])/255 for c in comp_order]

    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(
        composition_counts,
        autopct= autopct_filter,
        startangle=90,
        pctdistance=1.10,
        colors=pie_colors)

    ax.legend(
        composition_counts.index,
        title = "Classification",
        loc = "center left",
        bbox_to_anchor = (1, 0, 0.5, 1)
    )
    #[CHART2]
    st.pyplot(fig)


# Crater Calculator Page
def crater_calculator_page(page):
    st.title("Crater Calculator")
    st.subheader(
        "Disclaimer! \nThis calculator makes many assumptions about the trajectory, "
        "speed, volume, and surrounding physics of the meteorite. I am not accounting "
        "for drag force or the airburst that occurs when the meteorite hits the ground. "
        "Follow the link below if you wish for a more accurate representation."
    )

    meteorite_density = {
        'Carbonaceous Chondrites': 1000 * statistics.mean([2.11, 2.12, 3.1, 2.95, 2.95, 3.47]),
        'Enstatite Chondrites': 1000 * statistics.mean([3.55, 3.72]),
        'Ordinary Chondrites': 1000 * statistics.mean([3.21, 3.35, 3.40]),
        'Achondrites': 1000 * statistics.mean([3.12, 3.26, 2.86, 3.02, 3.05, 3.10, 3.32, 3.15]),
        'Stony-Iron': 1000 * statistics.mean([4.25, 4.76]),
        'Iron': 7500
    }
    # [DICTMETHOD] - Used .keys() here and .items() above
    # [ST1]
    meteorite_class = st.selectbox(
        "Select meteorite type:",
        list(meteorite_density.keys())
    )

    mass_kg = st.number_input(
        "Enter meteroite mass (kg):",
        min_value=0.01,
        value=100.0,
    )

    impact_velocity_kms = st.number_input(
        "Select impact velocity (km/s)",
        min_value=11.0,
        max_value=72.0,
        value=17.0,
        step=1.0
    )

    # Convert velocity to m/s
    velocity = impact_velocity_kms * 1000

    def estimate_density(selected_class):
        return meteorite_density.get(selected_class, 3320)

    def impact_energy(mass_kg, velocity):
        return 0.5 * mass_kg * velocity ** 2

    #[FUNC2P]
    def transient_crater_diameter(mass_kg, velocity, density_i, density_t=2500, g=9.81):
        """
               density_t = Assumed density of the ground being impacted (sedimentery rock)
               g = gravitational constant

               Pi-scaling law for transient crater diameter (meters) - (Holsapple, 2003)
               k is a constant that is applied to calibrate computations realistic Earth craters (comparing to the crater the
               Diablo Canyon meteorite created, which is included in the cited article on the website (Marvin and MacPherson, 1989)).
               This also required studying of the two other articles mentioned concerning formulas/calculations of crater volumes (Holsapple, 2003; Collins et al., 2005).
               These were referenced for assumed constants and how to configure formulas for calculating impact velocity. It took a lot of tweaking
               because I knew the Diablo Canyon meteorite from the CSV file was 30,000 kg and that it caused a 1.4 km diameter crater per Marvin and MacPherson (1989).
               I used the constant k and the collapse factor to account for expected scaling of the final diameter of the crater (Collins et al., 2005, pg 823). Basically,
               larger meteorites are those with a larger mass and larger density and therefore have a larger volume per the D = M/V formula. The idea behind the crater scaling
               is that because it assumes that some meteorites are largen enough to not be affected by the drag of the atmosphere as much. So this means that (A) it is not slowed
               down as much before hitting the ground (usually 11 km/s up to 72 km/s) and (B) that it has not been mostly disintegrated by flying through the atmosphere
               (as smaller meteorites do). This combination allows us to assume that the crater size is larger by a constant factor for larger meteorites.

               Long story short, I made a lot of "informed" guess and checks about the calcuation of the crater size and enery released on impact. I linked a more accurate calcuator
               on the "Crater Calculator" page.
               """
        k = 1.8  # empirical constant
        D_t = k * (density_i / density_t) ** (0.5) * (mass_kg / density_i) ** (1 / 3) * velocity ** 0.44 * g ** -0.22
        # D_t = Transient crater diameter, (Collins et al., 2005, pg 823)
        return D_t

    def final_crater_diameter(D_transient, collapse_factor=5.0):
        return D_transient * collapse_factor

    def energy_comparisons(E):
        tnt_equivalent = E / 4.184e6  # Joules to kg of TNT
        dynamite_equivalent = E / 2e6  # Joules to sticks of dynamite
        # {FUNCRETURN2] - This function returns two values of energy comparisons for the impact of the meteorite
        return tnt_equivalent, dynamite_equivalent

    # --- Calculations
    density = estimate_density(meteorite_class)
    E = impact_energy(mass_kg, velocity)
    D_transient = transient_crater_diameter(mass_kg, velocity, density)
    D_final = final_crater_diameter(D_transient)
    crater_area = math.pi * (D_final / 2) ** 2
    tnt_eq, dynamite_eq = energy_comparisons(E)

    # --- Display results
    st.subheader("Results")
    st.write(f"**Meteorite Type:** {meteorite_class}")
    st.write(f"**Density (kg/m³):** {density:,.0f}")
    st.write(f"**Impact Velocity (m/s):** {velocity:,.0f}")
    st.write(f"**Impact Energy (Joules):** {E:,.2e}")
    st.write(f"**TNT Equivalent (tons):** {tnt_eq:,.2f}")
    st.write(f"**Dynamite Equivalent (sticks of 2MJ):** {dynamite_eq:,.0f}")
    st.write(f"**Transient Crater Diameter (m):** {D_transient:,.2f}")
    st.write(f"**Final Crater Diameter (m):** {D_final:,.2f}")
    st.write(f"**Estimated Crater Area (m²):** {crater_area:,.2f}")


def largest_and_smallest_meteorites(df):
    if st.checkbox("Click to reveal the heaviest meteorite ever found!"):
        st.image("hoba.png")
        max_mass = df.loc[df["Mass (g)"].idxmax()]
        st.write(f"**Name:** {max_mass['Name']}")
        st.write(f"**Mass:** {int(max_mass['Mass (g)']/1000):,} kg")
        st.write(f"**Year:** {int(max_mass['Year'])}")
        st.write(f"**Latitude:** {max_mass['Lat']}")
        st.write(f"**Longitude:** {max_mass['Lon']}")
        st.write(f"**Location:** Northern Namibia, Africa  ")
        st.write(f"**Class:** {max_mass['Class']}")





# Comparison of Diablo Canyon: https://www.govinfo.gov/content/pkg/GOVPUB-SI-PURL-LPS116081/pdf/GOVPUB-SI-PURL-LPS116081.pdf (PG 116)
# More accurate calculator: https://impact.ese.ic.ac.uk/ImpactEarth/ImpactEffects/
# Reference and studying formulas to computer size: https://www.lpi.usra.edu/lunar/tools/lunarcratercalc/theory.pdf, https://impact.ese.ic.ac.uk/ImpactEarth/ImpactEffects/effects.pdf
# Website used for meteorite density: http://www.meteorites.com.au/odds&ends/density.html

def main():
    FILENAME = "Meteorite_Landings.csv"

    # Read the data
    df = read_meteorite_landings(FILENAME)
    df['class_norm'] = df['Class'].apply(normalize_class)
    df['Composition'] = df['class_norm'].apply(assign_category)

# Sidebar for page selection
    #[ST3]
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Meteorite Madness!","Statistics About Meteorites", "Map of Meteorite Landings", "Crater Calculator"]
    )

    # Home Page
    if page == "Meteorite Madness!":
            home_page(page)
    elif page == "Statistics About Meteorites":
            diagrams_page(df)
    elif page == "Map of Meteorite Landings":
            map_page(df)
    elif page == "Crater Calculator":
        crater_calculator_page(page)
        largest_and_smallest_meteorites(df)
        st.subheader("More accurate calculator:")
        st.write("https://impact.ese.ic.ac.uk/ImpactEarth/ImpactEffects/")
        st.subheader("Research articles referenced:")
        st.write("https://www.govinfo.gov/content/pkg/GOVPUB-SI-PURL-LPS116081/pdf/GOVPUB-SI-PURL-LPS116081.pdf" " (pg 116)")
        st.write("Equations and formulas referenced to compute crater size: https://www.lpi.usra.edu/lunar/tools/lunarcratercalc/theory.pdf, https://impact.ese.ic.ac.uk/ImpactEarth/ImpactEffects/effects.pdf")


if __name__ == "__main__":
    main()