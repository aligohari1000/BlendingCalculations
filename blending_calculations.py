import streamlit as st
import numpy as np

st.title("Blending Calculations")

# User selection for calculation type
calculation_type = st.selectbox(
    "Select the calculation you want to perform",
    ["RVP", "Flash Point", "Pour Point", "Cloud Point", "Aniline Point", "Smoke Point", "Viscosity"]
)

# Common input: flow rates
flow_rates = st.text_input("Enter flow rates (comma separated)", "5000, 4000, 6000, 7000")
flow_rates = [float(rate) for rate in flow_rates.split(",")]

# RVP Calculation
if calculation_type == "RVP":
    rvps = st.text_input("Enter RVP values (comma separated)", "11.1, 1.0, 2.8, 13.9")
    rvps = [float(rvp) for rvp in rvps.split(",")]

    def calculate_rvp_blend(rvps, flow_rates):
        rvp_indices = [rvp ** 1.25 for rvp in rvps]
        weighted_rvp_index = sum(flow_rate * rvp_index for flow_rate, rvp_index in zip(flow_rates, rvp_indices))
        blend_rvp = (weighted_rvp_index / sum(flow_rates)) ** (1 / 1.25)
        return blend_rvp

    rvp_blend = calculate_rvp_blend(rvps, flow_rates)
    st.write(f"Blended RVP: {rvp_blend:.2f} psi")

# Flash Point Calculation
elif calculation_type == "Flash Point":
    flash_points_celsius = st.text_input("Enter flash points in °C (comma separated)", "121.11, 26.67, 70.56")
    flash_points_celsius = [float(fp) for fp in flash_points_celsius.split(",")]

    def calculate_flash_point_index(flash_point):
        x = -0.06
        return flash_point ** (1 / x)

    def calculate_flash_point_blend(flash_points, flow_rates):
        flash_points_fahrenheit = [(fp * 9 / 5) + 32 for fp in flash_points]
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        flash_point_indices = [calculate_flash_point_index(fp) for fp in flash_points_fahrenheit]
        weighted_flash_point_index = sum(wf * index for wf, index in zip(weight_fractions, flash_point_indices))
        blend_flash_point_fahrenheit = weighted_flash_point_index ** x
        return (blend_flash_point_fahrenheit - 32) * 5 / 9

    blend_flash_point = calculate_flash_point_blend(flash_points_celsius, flow_rates)
    st.write(f"Blended Flash Point: {blend_flash_point:.2f} °C")

# Pour Point Calculation
elif calculation_type == "Pour Point":
    pour_points_celsius = st.text_input("Enter pour points in °C (comma separated)", "-15, -3, 42, 45")
    pour_points_celsius = [float(pp) for pp in pour_points_celsius.split(",")]

    def calculate_pour_point_index(pour_point):
        return 3262000 * ((pour_point / 1000) ** 12.5)

    def calculate_pour_point_blend(pour_points, flow_rates):
        pour_points_rankine = [(pp + 273.15) * 1.8 for pp in pour_points]
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        pour_point_indices = [calculate_pour_point_index(pp) for pp in pour_points_rankine]
        weighted_pour_point_index = sum(wf * index for wf, index in zip(weight_fractions, pour_point_indices))
        blended_pour_point_rankine = ((weighted_pour_point_index / 3262000) ** (1 / 12.5)) * 1000
        return (blended_pour_point_rankine / 1.8) - 273.15

    blended_pour_point = calculate_pour_point_blend(pour_points_celsius, flow_rates)
    st.write(f"Blended Pour Point: {blended_pour_point:.2f} °C")

# Cloud Point Calculation
elif calculation_type == "Cloud Point":
    cloud_points_celsius = st.text_input("Enter cloud points in °C (comma separated)", "-5, 5, 10")
    cloud_points_celsius = [float(cp) for cp in cloud_points_celsius.split(",")]

    def calculate_cloud_point_index(cloud_point):
        x = 0.05
        return cloud_point ** (1 / 0.05)

    def calculate_cloud_point_blend(cloud_points, flow_rates):
        cloud_points_kelvin = [(cp + 273.15) for cp in cloud_points]
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        cloud_point_indices = [calculate_cloud_point_index(cp) for cp in cloud_points_kelvin]
        weighted_cloud_point_index = sum(wf * index for wf, index in zip(weight_fractions, cloud_point_indices))
        blend_cloud_point_kelvin = weighted_cloud_point_index ** 0.05
        return blend_cloud_point_kelvin - 273.15

    blended_cloud_point = calculate_cloud_point_blend(cloud_points_celsius, flow_rates)
    st.write(f"Blended Cloud Point: {blended_cloud_point:.2f} °C")

# Aniline Point Calculation
elif calculation_type == "Aniline Point":
    aniline_points_celsius = st.text_input("Enter aniline points in °C (comma separated)", "71.0, 60.7, 36.8")
    aniline_points_celsius = [float(ap) for ap in aniline_points_celsius.split(",")]

    def calculate_aniline_point_index(aniline_point):
        return np.log(aniline_point + 273.15) / 0.00657

    def calculate_aniline_point_blend(aniline_points, flow_rates):
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        aniline_point_indices = [calculate_aniline_point_index(ap) for ap in aniline_points]
        weighted_aniline_point_index = sum(wf * index for wf, index in zip(weight_fractions, aniline_point_indices))
        blended_aniline_point = (np.exp(weighted_aniline_point_index * 0.00657)) - 273.15
        return blended_aniline_point

    blended_aniline_point = calculate_aniline_point_blend(aniline_points_celsius, flow_rates)
    st.write(f"Blended Aniline Point: {blended_aniline_point:.2f} °C")

# Smoke Point Calculation
elif calculation_type == "Smoke Point":
    specific_gravities = st.text_input("Enter specific gravities (comma separated)", "0.75, 0.8, 0.85")
    specific_gravities = [float(sg) for sg in specific_gravities.split(",")]
    aniline_point_blend = st.number_input("Enter blended aniline point in °C", value=56.54)

    def calculate_specific_gravity_blend(specific_gravities, flow_rates):
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        sg_blend = sum(wf * sg for wf, sg in zip(weight_fractions, specific_gravities))
        return sg_blend

    def calculate_smoke_point(ap_blend, sg_blend):
        return (
            -255.26 + 2.04 * ap_blend - 240.8 * np.log(sg_blend)
            + 7727 * (sg_blend / ap_blend)
        )

    sg_blend = calculate_specific_gravity_blend(specific_gravities, flow_rates)
    smoke_point_blend = calculate_smoke_point(aniline_point_blend, sg_blend)

    st.write(f"Blended Specific Gravity: {sg_blend:.3f}")
    st.write(f"Smoke Point of the Blend: {smoke_point_blend:.2f} mm")

# Viscosity Calculation
elif calculation_type == "Viscosity":
    viscosities = st.text_input("Enter viscosities in cSt (comma separated)", "75, 100, 200")
    viscosities = [float(v) for v in viscosities.split(",")]

    def calculate_viscosity_index(viscosity):
        return np.log10(viscosity) / (3 + np.log10(viscosity))

    def calculate_viscosity_blend_index(viscosities, flow_rates):
        total_flow_rate = sum(flow_rates)
        weight_fractions = [flow_rate / total_flow_rate for flow_rate in flow_rates]
        viscosity_indices = [calculate_viscosity_index(v) for v in viscosities]
        blended_viscosity_index = sum(wf * vi for wf, vi in zip(weight_fractions, viscosity_indices))
        return blended_viscosity_index

    def calculate_blended_viscosity(blended_viscosity_index):
        return 10 ** (3 * blended_viscosity_index / (1 - blended_viscosity_index))

    blended_viscosity_index = calculate_viscosity_blend_index(viscosities, flow_rates)
    blended_viscosity = calculate_blended_viscosity(blended_viscosity_index)

    st.write(f"Blended Viscosity Index: {blended_viscosity_index:.4f}")
    st.write(f"Blended Viscosity: {blended_viscosity:.2f} cSt")
