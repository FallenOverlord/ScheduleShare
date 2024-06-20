import streamlit as st
import streamlit.components.v1 as components

def show_ad():
    ad_code = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3034150478834245"
     crossorigin="anonymous"></script>
    <!-- Streamlit Ad -->
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-3034150478834245"
         data-ad-slot="YOUR_AD_SLOT"
         data-ad-format="auto"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    """
    components.html(ad_code, height=300)
