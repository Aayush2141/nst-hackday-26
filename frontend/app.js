/* Mandi Saathi — Core Frontend Application Logic */

"use strict";

// ── TRANSLATIONS (7 LANGUAGES) ──
const I18N = {
  en: {
    appTitle: "Mandi Saathi",
    tagline: "Find the best price for your crop",
    heroTagline: "All-India mandi prices, net of transport",
    lblCrop: "Crop",
    lblLocation: "Your Location",
    lblGeo: "Use GPS location",
    lblOr: "— or select —",
    lblState: "State",
    lblSelectState: "Select state…",
    lblDistrict: "District",
    lblSelectDistrict: "Select district…",
    lblRadius: "Search radius",
    lblRate: "Transport rate",
    lblWholeState: "Compare whole state",
    lblSearch: "Find best place to sell",
    lblMobileSearch: "Find best place to sell",
    lblBest: "Best place to sell",
    lblNetPrice: "Net price",
    lblUnit: "Rs/quintal",
    lblSpeak: "Listen",
    lblDownload: "Download CSV",
    lblMap: "Market map",
    lblChart: "Price trend",
    lblTable: "Nearby mandis",
    lblHowCalc: "How this was calculated",
    lblChipMarkets: "Markets",
    lblChipCrops: "Crops",
    lblChipUpdated: "Last updated",
    thRank: "#",
    thMarket: "Market",
    thState: "State",
    thDist: "Distance",
    thModal: "Modal",
    thTransport: "Transport",
    thNet: "Net",
    thDate: "Date",
    idleTitle: "Ready to find the best mandi",
    idleBody: "Select a crop and your location, then tap 'Find best place to sell'.",
    emptyTitle: "No mandis found nearby",
    emptyBody: "No price reports in this radius for this crop. Try increasing the search radius.",
    errTitle: "Something went wrong",
    lblRetry: "↺ Retry",
    bannerSample: "⚠️ Showing SAMPLE demo data across 8 states (not real-time Agmarknet prices).",
    bannerLive: (d, m, s) => `Live data from Agmarknet · last updated ${d}${m && s ? ` · ${m} markets across ${s} states` : ""}`,
    staleWarning: (d) => `⚠️ Note: Agmarknet data is more than 7 days old (latest: ${d}).`,
    gainBadge: (gain) => `+₹${gain}/q vs nearest mandi`,
    approxBadge: "≈ Approx. location",
    staleBadge: "Stale (>3d)",
    ttsPlaying: "Pause",
    ttsListen: "Listen",
    disclaimer: "Price guidance only — not a guaranteed outcome. Numbers computed in code; language model only explains. Distance is straight-line (haversine).",
  },
  hi: {
    appTitle: "मंडी साथी",
    tagline: "फसल बेचने का सबसे सही भाव",
    heroTagline: "अखिल भारतीय मंडी भाव, ढुलाई खर्च घटाकर",
    lblCrop: "फसल चुनें",
    lblLocation: "आपकी लोकेशन",
    lblGeo: "GPS लोकेशन उपयोग करें",
    lblOr: "— या चुनें —",
    lblState: "राज्य",
    lblSelectState: "राज्य चुनें…",
    lblDistrict: "ज़िला",
    lblSelectDistrict: "ज़िला चुनें…",
    lblRadius: "खोज का दायरा",
    lblRate: "ढुलाई दर",
    lblWholeState: "पूरे राज्य में तुलना करें",
    lblSearch: "बेचने की सबसे अच्छी जगह खोजें",
    lblMobileSearch: "सबसे अच्छी मंडी खोजें",
    lblBest: "बेचने की सर्वोत्तम मंडी",
    lblNetPrice: "शुद्ध भाव (ढुलाई काट कर)",
    lblUnit: "रुपये/क्विंटल",
    lblSpeak: "सुनें",
    lblDownload: "CSV डाउनलोड करें",
    lblMap: "मंडियों का नक्शा",
    lblChart: "भाव का रुझान",
    lblTable: "आस-पास की मंडियाँ",
    lblHowCalc: "यह गणना कैसे की गई?",
    lblChipMarkets: "मंडियाँ",
    lblChipCrops: "फसलें",
    lblChipUpdated: "अंतिम अपडेट",
    thRank: "#",
    thMarket: "मंडी",
    thState: "राज्य",
    thDist: "दूरी",
    thModal: "मंडी भाव",
    thTransport: "ढुलाई खर्च",
    thNet: "शुद्ध भाव",
    thDate: "दिनांक",
    idleTitle: "सर्वोत्तम मंडी खोजने के लिए तैयार",
    idleBody: "फसल और अपनी लोकेशन चुनें, फिर 'बेचने की सबसे अच्छी जगह खोजें' पर क्लिक करें।",
    emptyTitle: "पास में कोई मंडी नहीं मिली",
    emptyBody: "इस दायरे में इस फसल के भाव नहीं मिले। कृपया खोज का दायरा बढ़ाएँ।",
    errTitle: "कुछ गड़बड़ हुई",
    lblRetry: "↺ पुनः प्रयास करें",
    bannerSample: "⚠️ 8 राज्यों का नमूना (डेमो) डेटा दिखाया जा रहा है (Agmarknet का लाइव डेटा नहीं)।",
    bannerLive: (d, m, s) => `Agmarknet लाइव डेटा · अंतिम अपडेट ${d}${m && s ? ` · ${s} राज्यों की ${m} मंडियां` : ""}`,
    staleWarning: (d) => `⚠️ ध्यान दें: डेटा 7 दिनों से अधिक पुराना है (${d})।`,
    gainBadge: (gain) => `निकटतम मंडी से ₹${gain}/क्विंटल अधिक मुनाफा`,
    approxBadge: "≈ अनुमानित स्थान",
    staleBadge: "पुराना (>3 दिन)",
    ttsPlaying: "रोकें",
    ttsListen: "सुनें",
    disclaimer: "केवल मूल्य मार्गदर्शन — कोई गारंटी नहीं। सभी संख्याएँ कोड से तय होती हैं। दूरी हवाई (haversine) है।",
  },
  mr: {
    appTitle: "मंडी साथी",
    tagline: "तुमच्या शेतमालाला मिळवा योग्य भाव",
    heroTagline: "वाहतूक खर्च वजा जाता अखिल भारतीय मंडी भाव",
    lblCrop: "पीक निवडा",
    lblLocation: "तुमचे ठिकाण",
    lblGeo: "GPS लोकेशन वापरा",
    lblOr: "— किंवा निवडा —",
    lblState: "राज्य",
    lblSelectState: "राज्य निवडा…",
    lblDistrict: "जिल्हा",
    lblSelectDistrict: "जिल्हा निवडा…",
    lblRadius: "शोधाचे अंतर",
    lblRate: "वाहतूक दर",
    lblWholeState: "संपूर्ण राज्यात तुलना करा",
    lblSearch: "विक्रीसाठी सर्वोत्तम बाजार शोधा",
    lblMobileSearch: "सर्वोत्तम बाजार शोधा",
    lblBest: "विक्रीसाठी सर्वोत्तम बाजार",
    lblNetPrice: "निव्वळ भाव",
    lblUnit: "रुपये/क्विंटल",
    lblSpeak: "ऐका",
    lblDownload: "CSV डाउनलोड",
    lblMap: "बाजाराचा नकाशा",
    lblChart: "भावाचा कल",
    lblTable: "जवळपासचे बाजार",
    lblHowCalc: "हिशोब कसा केला?",
    lblChipMarkets: "बाजार",
    lblChipCrops: "पिके",
    lblChipUpdated: "शेवटचे अपडेट",
    thRank: "#",
    thMarket: "बाजार",
    thState: "राज्य",
    thDist: "अंतर",
    thModal: "बाजार भाव",
    thTransport: "वाहतूक खर्च",
    thNet: "निव्वळ भाव",
    thDate: "तारीख",
    idleTitle: "सर्वोत्तम बाजार शोधण्यासाठी तयार",
    idleBody: "पीक आणि तुमचे ठिकाण निवडून बटणावर क्लिक करा.",
    emptyTitle: "जवळपास बाजार सापडला नाही",
    emptyBody: "या अंतरामध्ये भाव उपलब्ध नाहीत. कृपया अंतर वाढवून पहा.",
    errTitle: "काहीतरी चूक झाली",
    lblRetry: "↺ पुन्हा प्रयत्न करा",
    bannerSample: "⚠️ नमुना (डेमो) डेटा दर्शविला जात आहे.",
    bannerLive: (d) => `✓ Agmarknet लाइव्ह डेटा · अपडेट: ${d}`,
    staleWarning: (d) => `⚠️ माहिती जुनी असू शकते (${d}).`,
    gainBadge: (gain) => `जवळच्या बाजारापेक्षा ₹${gain}/क्विंटल जास्त नफा`,
    approxBadge: "≈ अंदाजे स्थान",
    staleBadge: "जुना (>3 दिवस)",
    ttsPlaying: "थांबवा",
    ttsListen: "ऐका",
    disclaimer: "केवळ मार्गदर्शनासाठी. संख्या कोडद्वारे मोजल्या जातात.",
  },
  pa: {
    appTitle: "ਮੰਡੀ ਸਾਥੀ",
    tagline: "ਆਪਣੀ ਫਸਲ ਦਾ ਸਭ ਤੋਂ ਵਧੀਆ ਮੁੱਲ ਲੱਭੋ",
    heroTagline: "ਆਲ-ਇੰਡੀਆ ਮੰਡੀ ਭਾਅ, ਢੋਆ-ਢੁਆਈ ਖਰਚਾ ਕੱਟ ਕੇ",
    lblCrop: "ਫਸਲ ਚੁਣੋ",
    lblLocation: "ਤੁਹਾਡੀ ਲੋਕੇਸ਼ਨ",
    lblGeo: "GPS ਦੀ ਵਰਤੋਂ ਕਰੋ",
    lblOr: "— ਜਾਂ ਚੁਣੋ —",
    lblState: "ਸੂਬਾ",
    lblSelectState: "ਸੂਬਾ ਚੁਣੋ…",
    lblDistrict: "ਜ਼ਿਲ੍ਹਾ",
    lblSelectDistrict: "ਜ਼ਿਲ੍ਹਾ ਚੁਣੋ…",
    lblRadius: "ਖੋਜ ਦਾ ਘੇਰਾ",
    lblRate: "ਢੋਆ-ਢੁਆਈ ਦਰ",
    lblWholeState: "ਪੂਰੇ ਸੂਬੇ ਵਿੱਚ ਤੁਲਨਾ ਕਰੋ",
    lblSearch: "ਵੇਚਣ ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਮੰਡੀ ਲੱਭੋ",
    lblMobileSearch: "ਸਭ ਤੋਂ ਵਧੀਆ ਮੰਡੀ ਲੱਭੋ",
    lblBest: "ਵੇਚਣ ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਮੰਡੀ",
    lblNetPrice: "ਸ਼ੁੱਧ ਭਾਅ",
    lblUnit: "ਰੁਪਏ/ਕੁਇੰਟਲ",
    lblSpeak: "ਸੁਣੋ",
    lblDownload: "CSV ਡਾਊਨਲੋਡ",
    lblMap: "ਮੰਡੀਆਂ ਦਾ ਨਕਸ਼ਾ",
    lblChart: "ਭਾਅ ਦਾ ਰੁਝਾਨ",
    lblTable: "ਨੇੜਲੀਆਂ ਮੰਡੀਆਂ",
    lblHowCalc: "ਇਹ ਹਿਸਾਬ ਕਿਵੇਂ ਲਗਾਇਆ?",
    lblChipMarkets: "ਮੰਡੀਆਂ",
    lblChipCrops: "ਫਸਲਾਂ",
    lblChipUpdated: "ਆਖਰੀ ਅੱਪਡੇਟ",
    thRank: "#",
    thMarket: "ਮੰਡੀ",
    thState: "ਸੂਬਾ",
    thDist: "ਦੂਰੀ",
    thModal: "ਮੰਡੀ ਭਾਅ",
    thTransport: "ਢੋਆ-ਢੁਆਈ",
    thNet: "ਸ਼ੁੱਧ ਭਾਅ",
    thDate: "ਮਿਤੀ",
    idleTitle: "ਸਭ ਤੋਂ ਵਧੀਆ ਮੰਡੀ ਲੱਭਣ ਲਈ ਤਿਆਰ",
    idleBody: "ਫਸਲ ਅਤੇ ਆਪਣੀ ਲੋਕੇਸ਼ਨ ਚੁਣੋ।",
    emptyTitle: "ਨੇੜੇ ਕੋਈ ਮੰਡੀ ਨਹੀਂ ਮਿਲੀ",
    emptyBody: "ਖੋਜ ਦਾ ਘੇਰਾ ਵਧਾ ਕੇ ਦੇਖੋ।",
    errTitle: "ਕੁਝ ਗਲਤ ਹੋ ਗਿਆ",
    lblRetry: "↺ ਮੁੜ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
    bannerSample: "⚠️ ਡੈਮੋ ਡਾਟਾ ਦਿਖਾਇਆ ਜਾ ਰਿਹਾ ਹੈ।",
    bannerLive: (d) => `✓ Agmarknet ਲਾਈਵ ਡਾਟਾ · ਅੱਪਡੇਟ: ${d}`,
    staleWarning: (d) => `⚠️ ਡਾਟਾ ਪੁਰਾਣਾ ਹੋ ਸਕਦਾ ਹੈ (${d})।`,
    gainBadge: (gain) => `ਨੇੜਲੀ ਮੰਡੀ ਨਾਲੋਂ ₹${gain}/ਕੁਇੰਟਲ ਵੱਧ`,
    approxBadge: "≈ ਅੰਦਾਜ਼ਨ ਸਥਾਨ",
    staleBadge: "ਪੁਰਾਣਾ (>3 ਦਿਨ)",
    ttsPlaying: "ਰੋਕੋ",
    ttsListen: "ਸੁਣੋ",
    disclaimer: "ਸਿਰਫ਼ ਮਾਰਗਦਰਸ਼ਨ ਲਈ ਹੈ।",
  },
  gu: {
    appTitle: "મંડી સાથી",
    tagline: "તમારા પાક માટે શ્રેષ્ઠ ભાવ મેળવો",
    heroTagline: "ઓલ-ઇન્ડિયા બજાર ભાવ, પરિવહન ખર્ચ બાદ કરીને",
    lblCrop: "પાક પસંદ કરો",
    lblLocation: "તમારું સ્થાન",
    lblGeo: "GPS સ્થાન વાપરો",
    lblOr: "— અથવા પસંદ કરો —",
    lblState: "રાજ્ય",
    lblSelectState: "રાજ્ય પસંદ કરો…",
    lblDistrict: "જિલ્લો",
    lblSelectDistrict: "જિલ્લો પસંદ કરો…",
    lblRadius: "શોધ મર્યાદા",
    lblRate: "પરિવહન દર",
    lblWholeState: "સમગ્ર રાજ્યમાં સરખામણી કરો",
    lblSearch: "વેચવા માટે શ્રેષ્ઠ બજાર શોધો",
    lblMobileSearch: "શ્રેષ્ઠ બજાર શોધો",
    lblBest: "વેચાણ માટે શ્રેષ્ઠ માર્કેટ",
    lblNetPrice: "ચોખ્ખો ભાવ",
    lblUnit: "રૂપિયા/ક્વિન્ટલ",
    lblSpeak: "સાંભળો",
    lblDownload: "CSV ડાઉનલોડ",
    lblMap: "બજારોનો નકશો",
    lblChart: "ભાવનો ટ્રેન્ડ",
    lblTable: "નજીકના બજારો",
    lblHowCalc: "ગણતરી કેવી રીતે થઈ?",
    lblChipMarkets: "બજારો",
    lblChipCrops: "પાક",
    lblChipUpdated: "છેલ્લું અપડેટ",
    thRank: "#",
    thMarket: "બજાર",
    thState: "રાજ્ય",
    thDist: "અંતર",
    thModal: "બજાર ભાવ",
    thTransport: "પરિવહન ખર્ચ",
    thNet: "ચોખ્ખો ભાવ",
    thDate: "તારીખ",
    idleTitle: "શ્રેષ્ઠ બજાર શોધવા માટે તૈયાર",
    idleBody: "પાક અને સ્થાન પસંદ કરીને બટન દબાવો.",
    emptyTitle: "નજીકમાં કોઈ બજાર મળ્યું નથી",
    emptyBody: "કૃપા કરીને શોધ ત્રિજ્યા વધારીને જુઓ.",
    errTitle: "કંઈક ખોટું થયું",
    lblRetry: "↺ ફરી પ્રયાસ કરો",
    bannerSample: "⚠️ સેમ્પલ ડેમો ડેટા બતાવી રહ્યું છે.",
    bannerLive: (d) => `✓ Agmarknet લાઇવ ડેટા · અપડેટ: ${d}`,
    staleWarning: (d) => `⚠️ ડેટા 7 દિવસથી જૂનો છે (${d})।`,
    gainBadge: (gain) => `નજીકના બજાર કરતાં ₹${gain}/ક્વિન્ટલ વધુ નફો`,
    approxBadge: "≈ અંદાજિત સ્થાન",
    staleBadge: "જૂનો (>3 દિવસ)",
    ttsPlaying: "થોભો",
    ttsListen: "સાંભળો",
    disclaimer: "માત્ર માર્ગદર્શન માટે છે.",
  },
  ta: {
    appTitle: "மண்டி சாதி",
    tagline: "உங்கள் பயிருக்கு சிறந்த விலையைப் பெறுங்கள்",
    heroTagline: "போக்குவரத்து செலவு நீங்கலான அனைத்து இந்திய மண்டி விலைகள்",
    lblCrop: "பயிரைத் தேர்ந்தெடுக்கவும்",
    lblLocation: "உங்கள் இடம்",
    lblGeo: "GPS இருப்பிடத்தைப் பயன்படுத்தவும்",
    lblOr: "— அல்லது தேர்வு செய்க —",
    lblState: "மாநிலம்",
    lblSelectState: "மாநிலத்தைத் தேர்ந்தெடுக்கவும்…",
    lblDistrict: "மாவட்டம்",
    lblSelectDistrict: "மாவட்டத்தைத் தேர்ந்தெடுக்கவும்…",
    lblRadius: "தேடல் ஆரம்",
    lblRate: "போக்குவரத்து கட்டணம்",
    lblWholeState: "முழு மாநிலத்தையும் ஒப்பிடுக",
    lblSearch: "விற்க சிறந்த இடத்தை கண்டறியவும்",
    lblMobileSearch: "சிறந்த சந்தையைத் தேடுங்கள்",
    lblBest: "விற்பனைக்கு சிறந்த சந்தை",
    lblNetPrice: "நிகர விலை",
    lblUnit: "ரூபாய்/குவிண்டால்",
    lblSpeak: "கேளுங்கள்",
    lblDownload: "CSV பதிவிறக்கம்",
    lblMap: "சந்தை வரைபடம்",
    lblChart: "விலை போக்கு",
    lblTable: "அருகிலுள்ள சந்தைகள்",
    lblHowCalc: "இது எவ்வாறு கணக்கிடப்பட்டது?",
    lblChipMarkets: "சந்தைகள்",
    lblChipCrops: "பயிர்கள்",
    lblChipUpdated: "கடைசி புதுப்பிப்பு",
    thRank: "#",
    thMarket: "சந்தை",
    thState: "மாநிலம்",
    thDist: "தூரம்",
    thModal: "சந்தை விலை",
    thTransport: "போக்குவரத்து",
    thNet: "நிகர விலை",
    thDate: "தேதி",
    idleTitle: "சிறந்த சந்தையைக் கண்டறிய தயார்",
    idleBody: "பயிர் மற்றும் இடத்தை தேர்ந்தெடுத்து தேடுங்கள்.",
    emptyTitle: "அருகில் சந்தைகள் எதுவும் கிடைக்கவில்லை",
    emptyBody: "தேடல் ஆரத்தை அதிகரிக்க முயற்சிக்கவும்.",
    errTitle: "ஏதோ தவறு நடந்துவிட்டது",
    lblRetry: "↺ மீண்டும் முயற்சிக்கவும்",
    bannerSample: "⚠️ மாதிரி டெமோ தரவு காட்டப்படுகிறது.",
    bannerLive: (d) => `✓ Agmarknet நேரலை தரவு · புதுப்பிப்பு: ${d}`,
    staleWarning: (d) => `⚠️ தரவு பழையதாக இருக்கலாம் (${d}).`,
    gainBadge: (gain) => `அருகிலுள்ள சந்தையை விட ₹${gain}/குவிண்டால் அதிக லாபம்`,
    approxBadge: "≈ தோராயமான இடம்",
    staleBadge: "பழையது (>3 நாள்)",
    ttsPlaying: "நிறுத்து",
    ttsListen: "கேளுங்கள்",
    disclaimer: "விலை வழிகாட்டுதல் மட்டுமே — உத்தரவாதம் இல்லை.",
  },
  te: {
    appTitle: "మండి సాథీ",
    tagline: "మీ పంటకు ఉత్తమ ధరను పొందండి",
    heroTagline: "రవాణా ఖర్చు తీసివేసిన అఖిల భారత మార్కెట్ ధరలు",
    lblCrop: "పంటను ఎంచుకోండి",
    lblLocation: "మీ స్థానం",
    lblGeo: "GPS లొకేషన్ ఉపయోగించండి",
    lblOr: "— లేదా ఎంచుకోండి —",
    lblState: "రాష్ట్రం",
    lblSelectState: "రాష్ట్రాన్ని ఎంచుకోండి…",
    lblDistrict: "జిల్లా",
    lblSelectDistrict: "జిల్లాను ఎంచుకోండి…",
    lblRadius: "శోధన పరిధి",
    lblRate: "రవాణా ఛార్జీ",
    lblWholeState: "మొత్తం రాష్ట్రాన్ని సరిపోల్చండి",
    lblSearch: "అమ్మకానికి ఉత్తమ మార్కెట్ కనుగొనండి",
    lblMobileSearch: "ఉత్తమ మార్కెట్ కనుగొనండి",
    lblBest: "అమ్మకానికి ఉత్తమ మార్కెట్",
    lblNetPrice: "నికర ధర",
    lblUnit: "రూ./క్వింటాల్",
    lblSpeak: "వినండి",
    lblDownload: "CSV డౌన్‌లోడ్",
    lblMap: "మార్కెట్ మ్యాప్",
    lblChart: "ధర సరళి",
    lblTable: "సమీప మార్కెట్లు",
    lblHowCalc: "ఇది ఎలా లెక్కించబడింది?",
    lblChipMarkets: "మార్కెట్లు",
    lblChipCrops: "పంటలు",
    lblChipUpdated: "చివరి అప్‌డేట్",
    thRank: "#",
    thMarket: "మార్కెట్",
    thState: "రాష్ట్రం",
    thDist: "దూరం",
    thModal: "మార్కెట్ ధర",
    thTransport: "రవాణా ఖర్చు",
    thNet: "నికర ధర",
    thDate: "తేదీ",
    idleTitle: "ఉత్తమ మార్కెట్ కనుగొనడానికి సిద్ధం",
    idleBody: "పంట మరియు మీ లొకేషన్ ఎంచుకుని శోధించండి.",
    emptyTitle: "సమీపంలో మార్కెట్లు కనుగొనబడలేదు",
    emptyBody: "శోధన పరిధిని పెంచడానికి ప్రయత్నించండి.",
    errTitle: "ఏదో తప్పు జరిగింది",
    lblRetry: "↺ మళ్లీ ప్రయత్నించండి",
    bannerSample: "⚠️ డెమో డేటా చూపించబడుతోంది.",
    bannerLive: (d) => `✓ Agmarknet లైవ్ డేటా · అప్‌డేట్: ${d}`,
    staleWarning: (d) => `⚠️ డేటా పాతది కావచ్చు (${d}).`,
    gainBadge: (gain) => `సమీప మార్కెట్ కంటే ₹${gain}/క్వింటాల్ అధిక లాభం`,
    approxBadge: "≈ సుమారు స్థానం",
    staleBadge: "పాతది (>3 రోజులు)",
    ttsPlaying: "ఆపండి",
    ttsListen: "వినండి",
    disclaimer: "ధర మార్గదర్శకత్వం మాత్రమే.",
  },
};

// Top 40 crops with Hindi and regional synonyms
const CROP_LABELS = {
  Onion: { hi: "प्याज", mr: "कांदा", pa: "ਪਿਆਜ਼", gu: "ડુંગળી", ta: "வெங்காயம்", te: "ఉల్లిపాయ" },
  Tomato: { hi: "टमाटर", mr: "टोमॅटो", pa: "ਟਮਾਟਰ", gu: "ટમેટા", ta: "தக்காளி", te: "టమోటా" },
  Potato: { hi: "आलू", mr: "बटाटा", pa: "ਆਲੂ", gu: "બટાકા", ta: "உருளைக்கிழங்கு", te: "బంగాళాదుంప" },
  Wheat: { hi: "गेहूं", mr: "गहू", pa: "ਕਣਕ", gu: "ઘઉં", ta: "கோதுமை", te: "గోధుమలు" },
  Rice: { hi: "चावल / धान", mr: "तांदूळ", pa: "ਝੋਨਾ / ਚੌਲ", gu: "ચોખા", ta: "அரிசி", te: "వరి / బియ్యం" },
  Soybean: { hi: "सोयाबीन", mr: "सोयाबीन", pa: "ਸੋਇਆਬੀਨ", gu: "સોયાબીન", ta: "சோயாபீன்", te: "సోయాబీన్" },
  Cotton: { hi: "कपास", mr: "कापूस", pa: "ਕਪਾਹ", gu: "કપાસ", ta: "பருத்தி", te: "పత్తి" },
  Maize: { hi: "मक्का", mr: "मका", pa: "ਮੱਕੀ", gu: "મકાઈ", ta: "மக்காச்சோளம்", te: "మొక్కజొన్న" },
  Mustard: { hi: "सरसों", mr: "मोहरी", pa: "ਸਰ੍ਹੋਂ", gu: "રાઈ", ta: "கடுகு", te: "ఆవాలు" },
  Gram: { hi: "चना", mr: "हरभरा", pa: "ਛੋਲੇ", gu: "ચણા", ta: "கொண்டைக்கடலை", te: "శనగలు" },
  Chilli: { hi: "मिर्च", mr: "मिरची", pa: "ਮਿਰਚ", gu: "મરચાં", ta: "மிளகாய்", te: "మిరపకాయ" },
  Garlic: { hi: "लहसुन", mr: "लसूण", pa: "ਲਸਣ", gu: "લસણ", ta: "பூண்டு", te: "వెల్లుల్లి" },
  Ginger: { hi: "अदरक", mr: "आले", pa: "ਅਦਰਕ", gu: "આદુ", ta: "இஞ்சி", te: "అల్లం" },
  Turmeric: { hi: "हल्दी", mr: "हळद", pa: "ਹਲਦੀ", gu: "હળદર", ta: "மஞ்சள்", te: "పసుపు" },
};

// ── GLOBAL APPLICATION STATE ──
let currentLang = "en";
let appMeta = null;
let leafletMap = null;
let mapMarkers = [];
let userLocationMarker = null;
let routeLine = null;
let priceChart = null;
let currentResults = null;
let lastFailingCall = null;
let isSpeaking = false;
let speechUtterance = null;

// User origin coords (default to center of India if unset)
let userCoords = {
  lat: 22.9734,
  lon: 78.6569,
  state: null,
  district: null,
  isApprox: true,
};

// ── LOCAL STORAGE HELPERS ──
function getSaved(key, fallback = null) {
  try {
    return localStorage.getItem(key) || fallback;
  } catch (e) {
    return fallback;
  }
}

function setSaved(key, val) {
  try {
    localStorage.setItem(key, val);
  } catch (e) {
    // quota exceeded or disabled
  }
}

// ── TRANSLATION HELPER ──
function t(key, ...args) {
  const langDict = I18N[currentLang] || I18N.en;
  const val = langDict[key] !== undefined ? langDict[key] : (I18N.en[key] || key);
  if (typeof val === "function") {
    return val(...args);
  }
  return val;
}

function applyLanguage(newLang) {
  if (!I18N[newLang]) newLang = "en";
  currentLang = newLang;
  setSaved("ms_lang", currentLang);

  document.documentElement.lang = currentLang;

  // Update active lang button
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.lang === currentLang);
  });

  // Update static text in DOM
  const dict = I18N[currentLang];
  for (const [id, value] of Object.entries(dict)) {
    const el = document.getElementById(id);
    if (el && typeof value === "string") {
      el.textContent = value;
    }
  }

  // Update table header tooltips or text
  ["thRank", "thMarket", "thState", "thDist", "thModal", "thTransport", "thNet", "thDate"].forEach((id) => {
    const el = document.getElementById(id);
    if (el && dict[id]) el.textContent = dict[id];
  });

  // Re-render crop chips with regional labels
  renderPopularCrops();

  // If results are currently showing, update the explanation language
  if (currentResults && currentResults.best) {
    fetchExplanation();
  }

  // Update banner text
  renderBanners();
}

// ── TOAST NOTIFICATIONS ──
function showToast(message, isError = false) {
  const container = document.getElementById("toastContainer");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast ${isError ? "error" : ""}`;
  toast.setAttribute("role", "status");
  toast.innerHTML = `<span>${message}</span><div class="toast-progress"></div>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(20px)";
    toast.style.transition = "all 0.25s ease";
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}

// ── STATE MANAGEMENT ──
function setState(stateName) {
  const states = ["Idle", "Loading", "Error", "Empty", "Success"];
  states.forEach((s) => {
    const el = document.getElementById(`state${s}`);
    if (el) {
      if (s.toLowerCase() === stateName.toLowerCase()) {
        el.classList.remove("hidden");
      } else {
        el.classList.add("hidden");
      }
    }
  });
}

function showError(endpoint, err) {
  setState("error");
  const msgEl = document.getElementById("errMsg");
  const endEl = document.getElementById("errEndpoint");
  const rawEl = document.getElementById("errRaw");

  const errorText = err && err.message ? err.message : String(err);
  if (msgEl) msgEl.textContent = errorText;
  if (endEl) endEl.textContent = `API error on: ${endpoint}`;
  if (rawEl) rawEl.textContent = JSON.stringify({ endpoint, error: errorText, timestamp: new Date().toISOString() }, null, 2);

  lastFailingCall = () => fetchBestMandis();
  showToast(`Request failed: ${endpoint}`, true);
}

// ── INITIAL METADATA LOADING ──
async function loadAppMeta() {
  try {
    const res = await fetch("/api/meta");
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    appMeta = await res.json();

    // Populate stat chips with animated count-up
    const statMarkets = document.getElementById("statMarkets");
    const statCrops = document.getElementById("statCrops");
    const statUpdated = document.getElementById("statUpdated");

    if (statMarkets && appMeta.markets_count) animateNumber(statMarkets, appMeta.markets_count, 800);
    if (statCrops && appMeta.crops) animateNumber(statCrops, appMeta.crops.length, 800);
    if (statUpdated) statUpdated.textContent = appMeta.newest_price_date || appMeta.last_updated || "—";

    // Populate state select
    populateStateSelect();

    // Render banners
    renderBanners();

    // Render popular crops
    renderPopularCrops();

    // Restore saved settings
    restoreSavedInputs();

  } catch (err) {
    showError("/api/meta", err);
  }
}

function renderBanners() {
  if (!appMeta) return;

  const dataBanner = document.getElementById("dataBanner");
  const staleBanner = document.getElementById("staleBanner");

  if (dataBanner) {
    if (appMeta.banner === "sample" || appMeta.source === "seed") {
      dataBanner.className = "data-banner sample";
      dataBanner.textContent = t("bannerSample");
      dataBanner.classList.remove("hidden");
    } else {
      dataBanner.className = "data-banner live";
      dataBanner.innerHTML = `<span class="live-dot" aria-hidden="true"></span> <span>${t("bannerLive", appMeta.last_updated || appMeta.newest_price_date || "—", appMeta.markets_count, appMeta.states_count)}</span>`;
      dataBanner.classList.remove("hidden");
    }
  }

  if (staleBanner) {
    if (appMeta.stale) {
      staleBanner.textContent = t("staleWarning", appMeta.newest_price_date || "—");
      staleBanner.classList.remove("hidden");
    } else {
      staleBanner.classList.add("hidden");
    }
  }
}

// ── CROP AUTOCOMPLETE & CHIPS ──
function populateCropDropdown(filter = "") {
  const dropdown = document.getElementById("cropDropdown");
  if (!dropdown || !appMeta || !appMeta.crops) return;

  const q = filter.trim().toLowerCase();
  const matched = appMeta.crops.filter((c) => {
    if (!q) return true;
    if (c.toLowerCase().includes(q)) return true;
    const labels = CROP_LABELS[c];
    if (labels) {
      return Object.values(labels).some((l) => l.toLowerCase().includes(q));
    }
    return false;
  });

  dropdown.innerHTML = "";
  if (matched.length === 0) {
    dropdown.classList.add("hidden");
    return;
  }

  matched.slice(0, 10).forEach((crop) => {
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    const labelObj = CROP_LABELS[crop];
    const regional = labelObj && labelObj[currentLang] ? ` (${labelObj[currentLang]})` : (labelObj && labelObj.hi ? ` (${labelObj.hi})` : "");
    item.textContent = `${crop}${regional}`;
    item.onclick = () => selectCrop(crop);
    dropdown.appendChild(item);
  });

  dropdown.classList.remove("hidden");
}

function selectCrop(crop) {
  const input = document.getElementById("cropInput");
  const hidden = document.getElementById("cropValue");
  const dropdown = document.getElementById("cropDropdown");

  const labelObj = CROP_LABELS[crop];
  const regional = labelObj && labelObj[currentLang] ? ` (${labelObj[currentLang]})` : "";

  if (input) input.value = `${crop}${regional}`;
  if (hidden) hidden.value = crop;
  if (dropdown) dropdown.classList.add("hidden");

  setSaved("ms_last_crop", crop);

  // Update active chip
  document.querySelectorAll(".crop-chip").forEach((chip) => {
    chip.classList.toggle("active", chip.dataset.crop === crop);
  });
}

function renderPopularCrops() {
  const container = document.getElementById("cropChips");
  if (!container || !appMeta || !appMeta.crops) return;

  container.innerHTML = "";
  const popular = ["Onion", "Tomato", "Potato", "Wheat", "Soybean", "Rice", "Cotton", "Maize"];
  const available = popular.filter((p) => appMeta.crops.includes(p));
  const toShow = available.length > 0 ? available : appMeta.crops.slice(0, 6);

  const selectedCrop = document.getElementById("cropValue")?.value;

  toShow.forEach((crop) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = `crop-chip ${selectedCrop === crop ? "active" : ""}`;
    chip.dataset.crop = crop;
    const labelObj = CROP_LABELS[crop];
    const regional = labelObj && labelObj[currentLang] ? labelObj[currentLang] : (labelObj && labelObj.hi ? labelObj.hi : crop);
    chip.textContent = `${crop} (${regional})`;
    chip.onclick = () => selectCrop(crop);
    container.appendChild(chip);
  });
}

// ── LOCATION SELECTORS & GEOCODING ──
function populateStateSelect() {
  const sel = document.getElementById("stateSelect");
  if (!sel || !appMeta || !appMeta.states) return;

  sel.innerHTML = `<option value="">${t("lblSelectState")}</option>`;
  appMeta.states.forEach((st) => {
    const opt = document.createElement("option");
    opt.value = st;
    opt.textContent = st;
    sel.appendChild(opt);
  });
}

function onStateChanged() {
  const stateSel = document.getElementById("stateSelect");
  const distSel = document.getElementById("districtSelect");
  const geoBtn = document.getElementById("geoBtn");
  if (!stateSel || !distSel) return;

  if (geoBtn) geoBtn.classList.remove("active");

  const state = stateSel.value;
  distSel.innerHTML = `<option value="">${t("lblSelectDistrict")}</option>`;

  if (!state) {
    distSel.disabled = true;
    return;
  }

  // Filter districts belonging to this state
  const districts = (appMeta.districts || [])
    .filter((d) => d.state.toLowerCase() === state.toLowerCase())
    .map((d) => d.district);

  const uniqueDistricts = [...new Set(districts)].sort();
  uniqueDistricts.forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = d;
    distSel.appendChild(opt);
  });

  distSel.disabled = false;
}

async function onDistrictChanged() {
  const stateSel = document.getElementById("stateSelect");
  const distSel = document.getElementById("districtSelect");
  const locStatus = document.getElementById("locStatus");
  const geoBtn = document.getElementById("geoBtn");
  if (!stateSel || !distSel) return;

  const state = stateSel.value;
  const district = distSel.value;
  if (!state || !district) return;

  if (geoBtn) geoBtn.classList.remove("active");
  if (locStatus) locStatus.textContent = `Resolving coordinates for ${district}…`;

  try {
    const res = await fetch(`/api/geocode?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    userCoords = {
      lat: data.lat,
      lon: data.lon,
      state: state,
      district: district,
      isApprox: data.approximate || false,
      source: "manual",
    };

    if (locStatus) {
      locStatus.innerHTML = `<span class="loc-badge manual">📍 Selected District: ${district}, ${state} (Overrides GPS)</span>`;
    }

    setSaved("ms_last_loc", JSON.stringify(userCoords));

    if (leafletMap) {
      updateUserMarkerOnMap();
      leafletMap.setView([userCoords.lat, userCoords.lon], 8);
    }
  } catch (err) {
    if (locStatus) locStatus.textContent = `Could not geocode ${district}. Using fallback.`;
    showToast(`Geocoding error for ${district}`, true);
  }
}

function useGpsLocation() {
  const locStatus = document.getElementById("locStatus");
  const geoBtn = document.getElementById("geoBtn");
  const stateSel = document.getElementById("stateSelect");
  const distSel = document.getElementById("districtSelect");

  if (!navigator.geolocation) {
    showToast("GPS is not supported by your browser.", true);
    return;
  }

  if (locStatus) locStatus.textContent = "Requesting GPS position…";

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userCoords = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
        state: null,
        district: null,
        isApprox: false,
        source: "gps",
      };

      if (geoBtn) geoBtn.classList.add("active");
      if (stateSel) stateSel.value = "";
      if (distSel) {
        distSel.innerHTML = `<option value="">${t("lblSelectDistrict")}</option>`;
        distSel.disabled = true;
      }

      if (locStatus) {
        locStatus.innerHTML = `<span class="loc-badge gps">📍 GPS Active: ${userCoords.lat.toFixed(4)}, ${userCoords.lon.toFixed(4)} (Overrides dropdowns)</span>`;
      }

      setSaved("ms_last_loc", JSON.stringify(userCoords));
      showToast("Location updated via GPS");

      if (leafletMap) {
        updateUserMarkerOnMap();
        leafletMap.setView([userCoords.lat, userCoords.lon], 9);
      }
    },
    (err) => {
      if (locStatus) locStatus.textContent = "GPS access denied. Pick state & district.";
      showToast("GPS permission denied or unavailable.", true);
    },
    { timeout: 10000, enableHighAccuracy: true }
  );
}

// ── RESTORE SAVED PREFERENCES ──
function restoreSavedInputs() {
  const savedCrop = getSaved("ms_last_crop");
  if (savedCrop && appMeta && appMeta.crops && appMeta.crops.includes(savedCrop)) {
    selectCrop(savedCrop);
  } else if (appMeta && appMeta.crops && appMeta.crops.length > 0) {
    selectCrop(appMeta.crops[0]);
  }

  const savedLoc = getSaved("ms_last_loc");
  if (savedLoc) {
    try {
      const parsed = JSON.parse(savedLoc);
      if (parsed && typeof parsed.lat === "number" && typeof parsed.lon === "number") {
        userCoords = parsed;
        const locStatus = document.getElementById("locStatus");
        if (locStatus) {
          locStatus.textContent = userCoords.district
            ? `📍 ${userCoords.district}, ${userCoords.state}`
            : `📍 ${userCoords.lat.toFixed(3)}, ${userCoords.lon.toFixed(3)}`;
        }
        if (userCoords.state) {
          const stateSel = document.getElementById("stateSelect");
          if (stateSel) {
            stateSel.value = userCoords.state;
            onStateChanged();
            if (userCoords.district) {
              const distSel = document.getElementById("districtSelect");
              if (distSel) distSel.value = userCoords.district;
            }
          }
        }
      }
    } catch (e) {
      // ignore JSON parse error
    }
  }
}

// ── MAP INITIALIZATION & RENDERING ──
function initLeafletMap() {
  const mapEl = document.getElementById("map");
  if (!mapEl || leafletMap) return;

  leafletMap = L.map("map", {
    scrollWheelZoom: false,
  }).setView([userCoords.lat, userCoords.lon], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(leafletMap);

  // Drop pin on map click
  leafletMap.on("click", (e) => {
    userCoords = {
      lat: e.latlng.lat,
      lon: e.latlng.lng,
      state: null,
      district: null,
      isApprox: false,
    };
    const locStatus = document.getElementById("locStatus");
    if (locStatus) {
      locStatus.textContent = `📍 Map pin: ${userCoords.lat.toFixed(4)}, ${userCoords.lon.toFixed(4)}`;
    }
    setSaved("ms_last_loc", JSON.stringify(userCoords));
    updateUserMarkerOnMap();
    showToast("Location updated from map pin");
  });
}

function updateUserMarkerOnMap() {
  if (!leafletMap) return;
  if (userLocationMarker) userLocationMarker.remove();

  userLocationMarker = L.circleMarker([userCoords.lat, userCoords.lon], {
    radius: 9,
    color: "#0e3421",
    fillColor: "#f59e0b",
    fillOpacity: 1,
    weight: 3,
    className: "map-user-marker",
  })
    .addTo(leafletMap)
    .bindPopup(`<strong>Your Location / आपकी लोकेशन</strong><br>${userCoords.lat.toFixed(4)}, ${userCoords.lon.toFixed(4)}`);
}

function colorForRank(rank) {
  if (rank === 1) return "#1b5e3b";
  if (rank === 2) return "#2563eb";
  if (rank === 3) return "#0891b2";
  return "#64748b";
}

function renderResultsOnMap(rows, best) {
  if (!leafletMap) return;

  // Clear old markers
  mapMarkers.forEach((m) => m.remove());
  mapMarkers = [];
  if (routeLine) routeLine.remove();

  updateUserMarkerOnMap();

  const bounds = [[userCoords.lat, userCoords.lon]];

  rows.forEach((row) => {
    if (row.lat && row.lon) {
      bounds.push([row.lat, row.lon]);
      const color = colorForRank(row.rank);
      const isBest = row.rank === 1;

      const marker = L.circleMarker([row.lat, row.lon], {
        radius: isBest ? 13 : 8,
        color: "#ffffff",
        fillColor: color,
        fillOpacity: 0.95,
        weight: isBest ? 3 : 2,
        className: isBest ? "map-best-marker" : "",
      }).addTo(leafletMap);

      marker.bindPopup(`
        <div style="font-family: sans-serif; font-size: 13px;">
          <strong>#${row.rank} ${row.market}</strong> (${row.district}, ${row.state})<br/>
          <span style="color: #1b5e3b; font-weight: bold; font-size: 15px;">Net: ₹${row.net_price}</span> /quintal<br/>
          Modal: ₹${row.modal_price} · Transport: ₹${row.transport_cost}<br/>
          Distance: ${row.distance_km} km ${row.approximate_location ? "<em>(approx)</em>" : ""}<br/>
          Date: ${row.price_date || row.arrival_date || "—"}
        </div>
      `);

      marker.on("click", () => {
        loadPriceTrend(row.crop || row.commodity || document.getElementById("cropValue").value, row.market);
      });

      mapMarkers.push(marker);
    }
  });

  // Draw dashed polyline to best mandi
  if (best && best.lat && best.lon) {
    routeLine = L.polyline(
      [
        [userCoords.lat, userCoords.lon],
        [best.lat, best.lon],
      ],
      {
        color: "#1b5e3b",
        weight: 3.5,
        dashArray: "6, 8",
        opacity: 0.85,
        className: "animated-route",
      }
    ).addTo(leafletMap);
  }

  if (bounds.length > 1) {
    leafletMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 10 });
  }
}

// ── PRICE CHART (CHART.JS) ──
let currentChartDays = 30;
let currentChartMarket = null;
let currentChartCrop = null;

async function loadPriceTrend(crop, market, days = 30) {
  currentChartMarket = market;
  currentChartCrop = crop || document.getElementById("cropValue")?.value || "";
  currentChartDays = days;

  const lbl = document.getElementById("chartMarket");
  if (lbl) lbl.textContent = `${market} · ${crop} (${days} days)`;

  // Update tabs
  document.getElementById("tab30")?.classList.toggle("active", days === 30);
  document.getElementById("tab7")?.classList.toggle("active", days === 7);

  try {
    const res = await fetch(`/api/trend?crop=${encodeURIComponent(crop)}&market=${encodeURIComponent(market)}&days=${days}&lang=${currentLang}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderChart(data);
  } catch (err) {
    console.error("Trend error:", err);
    renderChart({ points: [], market: market, crop: crop });
  }
}

function renderChart(trendData) {
  const canvas = document.getElementById("chart");
  const chartWrap = document.getElementById("chartWrap");
  const chartNote = document.getElementById("chartNote");
  if (!canvas) return;

  if (priceChart) {
    priceChart.destroy();
    priceChart = null;
  }

  const points = (trendData && (trendData.points || trendData.series)) || [];

  // Empty state handling
  let emptyMsg = document.getElementById("chartEmptyMsg");
  if (points.length === 0) {
    canvas.style.display = "none";
    if (!emptyMsg && chartWrap) {
      emptyMsg = document.createElement("div");
      emptyMsg.id = "chartEmptyMsg";
      emptyMsg.className = "chart-empty-msg";
      chartWrap.appendChild(emptyMsg);
    }
    if (emptyMsg) {
      emptyMsg.textContent = `No price trend data recorded for ${currentChartMarket || "this market"} in the selected ${currentChartDays}-day period.`;
      emptyMsg.style.display = "flex";
    }
    if (chartNote) chartNote.classList.add("hidden");
    return;
  }

  if (emptyMsg) emptyMsg.style.display = "none";
  canvas.style.display = "block";

  const isSingle = points.length === 1;
  const labels = points.map((s) => (s.date ? s.date.slice(5) : "")); // MM-DD
  const modalPrices = points.map((s) => s.modal_price);
  const minPrices = points.map((s) => (s.min_price !== undefined ? s.min_price : s.modal_price));
  const maxPrices = points.map((s) => (s.max_price !== undefined ? s.max_price : s.modal_price));

  // Compute 7-day moving average or use backend ma7
  const movingAvg = points.map((s, i) => {
    if (s.ma7 !== undefined && s.ma7 !== null) return s.ma7;
    const start = Math.max(0, i - 6);
    const window = modalPrices.slice(start, i + 1);
    const avg = window.reduce((a, b) => a + b, 0) / window.length;
    return Math.round(avg * 100) / 100;
  });

  if (chartNote) {
    if (isSingle) {
      chartNote.textContent = `📅 Showing reported price on ${points[0].date}. Multi-day trend will automatically accumulate across daily arrivals.`;
      chartNote.classList.remove("hidden");
    } else {
      chartNote.classList.add("hidden");
    }
  }

  if (typeof Chart === "undefined") {
    console.warn("Chart.js not available");
    return;
  }

  const isDark = document.documentElement.classList.contains("dark");
  const textColor = isDark ? "#eaf1ec" : "#15241b";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.06)";
  const primaryLine = isDark ? "#2ea063" : "#1b5e3b";
  const primaryFill = isDark ? "rgba(46, 160, 99, 0.15)" : "rgba(27, 94, 59, 0.1)";
  const maLine = isDark ? "#f59e0b" : "#d97706";

  const datasets = [
    {
      label: "Modal Price (₹/q)",
      data: modalPrices,
      borderColor: primaryLine,
      backgroundColor: primaryFill,
      borderWidth: 2.5,
      tension: isSingle ? 0 : 0.25,
      pointRadius: isSingle ? 8 : (points.length < 10 ? 5 : 3),
      pointHoverRadius: isSingle ? 10 : 7,
      pointBackgroundColor: primaryLine,
      pointBorderColor: "#ffffff",
      pointBorderWidth: isSingle ? 2 : 1,
      fill: !isSingle,
    },
  ];

  if (!isSingle) {
    datasets.push({
      label: "7-Day Moving Avg",
      data: movingAvg,
      borderColor: maLine,
      borderWidth: 2,
      borderDash: [4, 4],
      pointRadius: 0,
      fill: false,
    });
    datasets.push({
      label: "Min Price Band",
      data: minPrices,
      borderColor: "transparent",
      backgroundColor: isDark ? "rgba(46, 160, 99, 0.08)" : "rgba(27, 94, 59, 0.05)",
      pointRadius: 0,
      fill: "+1",
    });
    datasets.push({
      label: "Max Price Band",
      data: maxPrices,
      borderColor: "transparent",
      backgroundColor: "transparent",
      pointRadius: 0,
      fill: false,
    });
  }

  priceChart = new Chart(canvas, {
    type: "line",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 900,
        easing: "easeOutQuart",
      },
      plugins: {
        legend: {
          display: !isSingle,
          position: "top",
          labels: {
            color: textColor,
            font: { size: 11, family: "Inter" },
            filter: (item) => !item.text.includes("Band"),
          },
        },
        tooltip: {
          mode: "index",
          intersect: false,
          callbacks: {
            label: function (context) {
              const val = context.parsed.y;
              if (val === null || val === undefined) return "";
              const formatted = "₹" + Math.round(val).toLocaleString("en-IN") + "/q";
              if (context.dataset.label.includes("Modal")) {
                return `Modal Price: ${formatted}`;
              } else if (context.dataset.label.includes("Moving")) {
                return `7-Day Avg: ${formatted}`;
              } else if (context.dataset.label.includes("Min")) {
                return `Min Price: ${formatted}`;
              } else if (context.dataset.label.includes("Max")) {
                return `Max Price: ${formatted}`;
              }
              return `${context.dataset.label}: ${formatted}`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { size: 11 } },
        },
        y: {
          grid: { color: gridColor },
          ticks: {
            color: textColor,
            font: { size: 11 },
            callback: (val) => "₹" + Math.round(val).toLocaleString("en-IN"),
          },
        },
      },
    },
  });
}

// ── SEARCH EXECUTION (/api/best & /api/explain) ──
async function fetchBestMandis() {
  const crop = document.getElementById("cropValue")?.value;
  if (!crop) {
    showToast("Please select a crop first.", true);
    return;
  }

  const radius = parseFloat(document.getElementById("radiusSlider")?.value || "300");
  const rate = parseFloat(document.getElementById("rateSlider")?.value || "2.5");

  const searchBtn = document.getElementById("searchBtn");
  const spinner = document.getElementById("btnSpinner");
  const searchBtnText = document.getElementById("lblSearch");
  const origSearchText = searchBtnText ? searchBtnText.textContent : "";

  if (spinner) spinner.classList.remove("hidden");
  if (searchBtn) searchBtn.disabled = true;

  setState("loading");

  try {
    const url = `/api/best?crop=${encodeURIComponent(crop)}&lat=${userCoords.lat}&lon=${userCoords.lon}&rate=${rate}&radius=${radius}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    const data = await res.json();
    currentResults = data;

    if (!data.best || !data.ranked || data.ranked.length === 0) {
      setState("empty");
      const emptyBody = document.getElementById("emptyBody");
      if (emptyBody) {
        if (data.nearest_state_with_data) {
          emptyBody.textContent = `No mandis reporting ${crop} within ${radius} km. The nearest state with data is ${data.nearest_state_with_data}. Try expanding your search radius to 1000 km.`;
        } else {
          emptyBody.textContent = t("emptyBody");
        }
      }
      return;
    }

    setState("success");
    renderSuccessView(data, crop, rate, radius);

  } catch (err) {
    showError("/api/best", err);
  } finally {
    if (spinner) spinner.classList.add("hidden");
    if (searchBtn) searchBtn.disabled = false;
  }
}

function animateNumber(element, target, duration = 800) {
  if (!element) return;
  const start = 0;
  const startTime = performance.now();

  function update(time) {
    const elapsed = time - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Smooth exponential decay easing
    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const current = Math.floor(start + (target - start) * easeProgress);
    element.textContent = current.toLocaleString("en-IN");
    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = target.toLocaleString("en-IN");
    }
  }

  requestAnimationFrame(update);
}

function renderSuccessView(data, crop, rate, radius) {
  const best = data.best;
  const runnerUp = data.runner_up;
  const ranked = data.ranked || [];

  // Hero Card entrance pop
  const heroCard = document.getElementById("bestPlaceCard");
  if (heroCard) {
    heroCard.classList.remove("hero-pop");
    void heroCard.offsetWidth; // trigger reflow
    heroCard.classList.add("hero-pop");
  }

  // 1. Hero Card fields
  const bestMarket = document.getElementById("bestMarket");
  const bestLocation = document.getElementById("bestLocation");
  const bestNet = document.getElementById("bestNet");
  const bestDist = document.getElementById("bestDist");
  const bestTransport = document.getElementById("bestTransport");
  const bestDate = document.getElementById("bestDate");
  const trendBadge = document.getElementById("trendBadge");
  const gainBadge = document.getElementById("gainBadge");
  const staleBadge = document.getElementById("staleBadge");
  const approxBadge = document.getElementById("approxBadge");

  if (bestMarket) bestMarket.textContent = best.market;
  if (bestLocation) bestLocation.textContent = `${best.district}, ${best.state}`;

  if (bestNet) animateNumber(bestNet, Math.round(best.net_price), 800);
  if (bestDist) bestDist.textContent = `${best.distance_km} km`;
  if (bestTransport) bestTransport.textContent = `Transport: ₹${best.transport_cost}/q`;
  if (bestDate) bestDate.textContent = best.price_date || best.arrival_date || "Recent";

  // Trend Badge with subtle micro-bounce
  if (trendBadge && data.trend) {
    const sig = data.trend.signal || "flat";
    const arrow = sig === "rising" ? "▲" : sig === "falling" ? "▼" : "●";
    const pctVal = data.trend.percent_change_7d !== undefined ? data.trend.percent_change_7d : data.trend.pct_change;
    const pct = pctVal !== undefined && pctVal !== null ? ` (${pctVal > 0 ? "+" : ""}${pctVal}%)` : "";
    const bounceClass = sig === "rising" ? " trend-bounce-up" : sig === "falling" ? " trend-bounce-down" : " trend-pulse";
    trendBadge.className = `trend-badge ${sig}${bounceClass}`;
    trendBadge.textContent = `${arrow} ${t(sig)} ${pct}`;
  }

  // Gain Badge with pop bounce
  if (gainBadge) {
    if (data.difference_rs && data.difference_rs > 0) {
      gainBadge.textContent = t("gainBadge", Math.round(data.difference_rs));
      gainBadge.className = "gain-badge gain-bounce";
      gainBadge.classList.remove("hidden");
    } else {
      gainBadge.classList.add("hidden");
    }
  }

  // Stale & Approx badges
  if (staleBadge) {
    staleBadge.classList.toggle("hidden", !(best.days_old && best.days_old > 3));
    staleBadge.textContent = t("staleBadge");
  }
  if (approxBadge) {
    approxBadge.classList.toggle("hidden", !best.approximate_location);
    approxBadge.textContent = t("approxBadge");
  }

  // Calculation details
  renderCalculation(best, rate);

  // Render Map
  initLeafletMap();
  setTimeout(() => {
    leafletMap.invalidateSize();
    renderResultsOnMap(ranked, best);
  }, 100);

  // Render Table
  renderTable(ranked);

  // Load Trend Chart
  loadPriceTrend(crop, best.market, 30);

  // Pre-populate explanation immediately so it is never blank!
  const explainText = document.getElementById("explainText");
  const explainSource = document.getElementById("explainSource");
  const hintText = document.getElementById("hintText");

  if (explainText) {
    explainText.textContent = data.explanation || "Optimal mandi calculated from modal price and transport distance.";
  }
  if (explainSource) {
    explainSource.textContent = "Generated by verified calculation template";
  }
  if (hintText && data.trend && data.trend.hint) {
    const hintObj = data.trend.hint;
    const hintStr = typeof hintObj === "string" ? hintObj : (hintObj.text || hintObj.text_en || "");
    if (hintStr) hintText.textContent = `💡 Hint: ${hintStr}`;
  }

  // Fetch LLM / Template Explanation asynchronously
  fetchExplanation();
}

function renderCalculation(best, rate) {
  const content = document.getElementById("calcContent");
  if (!content) return;

  const modal = best.modal_price;
  const dist = best.distance_km;
  const trans = best.transport_cost;
  const net = best.net_price;

  content.innerHTML = `
    <p>We compute the <strong>Net Farmer Price</strong> by subtracting the straight-line transport cost from the latest reported mandi modal price:</p>
    <div class="calc-formula">
      Net Price = Modal Price (₹${modal}) − [ Distance (${dist} km) × Rate (₹${rate}/q/km) ]<br/>
      Net Price = ₹${modal} − ₹${trans} = <strong>₹${net} / quintal</strong>
    </div>
    <p style="font-size:0.82rem; margin-top:8px;">
      Distance is computed using the great-circle Haversine formula from your coordinates (${userCoords.lat.toFixed(2)}, ${userCoords.lon.toFixed(2)}) to ${best.district}. 
      ${best.approximate_location ? "<em>Note: State centroid coordinates were used as approximate market location.</em>" : ""}
    </p>
  `;
}

// ── RANKED TABLE ──
let currentSortCol = "net_price";
let currentSortAsc = false;

function renderTable(rows) {
  const tbody = document.getElementById("tableBody");
  if (!tbody) return;

  tbody.innerHTML = "";

  // Sort rows
  const sorted = [...rows].sort((a, b) => {
    let valA = a[currentSortCol];
    let valB = b[currentSortCol];
    if (typeof valA === "string") valA = valA.toLowerCase();
    if (typeof valB === "string") valB = valB.toLowerCase();
    if (valA < valB) return currentSortAsc ? -1 : 1;
    if (valA > valB) return currentSortAsc ? 1 : -1;
    return 0;
  });

  sorted.forEach((row, idx) => {
    const tr = document.createElement("tr");
    tr.style.setProperty("--row-index", idx);
    if (row.rank === 1) tr.className = "best-row";

    const medal = row.rank === 1 ? "🥇" : row.rank === 2 ? "🥈" : row.rank === 3 ? "🥉" : "";
    const staleTag = row.days_old && row.days_old > 3 ? ` <span class="stale-badge">${t("staleBadge")}</span>` : "";
    const approxTag = row.approximate_location ? ` <span class="approx-badge">≈</span>` : "";

    tr.innerHTML = `
      <td class="rank-cell">${medal} ${row.rank}</td>
      <td><strong>${row.market}</strong>${approxTag}</td>
      <td>${row.state}</td>
      <td>${row.distance_km} km</td>
      <td>₹${row.modal_price}</td>
      <td>₹${row.transport_cost}</td>
      <td><strong style="color:var(--primary)">₹${row.net_price}</strong></td>
      <td>${row.price_date || row.arrival_date || "—"}${staleTag}</td>
    `;

    tr.onclick = () => {
      // Focus on map & chart with smooth flyTo animation
      if (leafletMap && row.lat && row.lon) {
        leafletMap.flyTo([row.lat, row.lon], 9, { duration: 1.2, easeLinearity: 0.25 });
      }
      loadPriceTrend(row.crop || row.commodity || document.getElementById("cropValue").value, row.market);
    };

    tbody.appendChild(tr);
  });
}

function setupTableSorting() {
  document.querySelectorAll("th.sortable").forEach((th) => {
    th.addEventListener("click", () => {
      const col = th.dataset.col;
      if (currentSortCol === col) {
        currentSortAsc = !currentSortAsc;
      } else {
        currentSortCol = col;
        currentSortAsc = false;
      }
      if (currentResults && currentResults.ranked) {
        renderTable(currentResults.ranked);
      }
    });
  });
}

// ── EXPLANATION & SPEECH (TTS) ──
async function fetchExplanation() {
  if (!currentResults || !currentResults.best) return;

  const explainText = document.getElementById("explainText");
  const explainSource = document.getElementById("explainSource");
  const hintText = document.getElementById("hintText");

  const crop = document.getElementById("cropValue")?.value;
  const radius = parseFloat(document.getElementById("radiusSlider")?.value || "300");
  const rate = parseFloat(document.getElementById("rateSlider")?.value || "2.5");

  try {
    const res = await fetch("/api/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        crop: crop,
        lat: userCoords.lat,
        lon: userCoords.lon,
        rate: rate,
        radius: radius,
        lang: currentLang,
      }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (explainText && data.explanation) {
      explainText.textContent = data.explanation;
    }
    if (explainSource) {
      explainSource.textContent = data.source === "llm" ? "Generated by local Ollama (verified numbers)" : "Generated by verified calculation template";
    }
    if (hintText && data.hint) {
      hintText.textContent = `💡 Hint: ${data.hint}`;
    }
  } catch (err) {
    console.warn("LLM explanation request failed, using template:", err);
  }
}

function toggleSpeech() {
  const btn = document.getElementById("speakBtn");
  const textEl = document.getElementById("explainText");
  const soundwave = document.getElementById("soundwave");
  if (!btn || !textEl) return;

  function resetSpeechUI() {
    isSpeaking = false;
    btn.innerHTML = `🔊 <span id="lblSpeak">${t("ttsListen")}</span>`;
    if (soundwave) {
      soundwave.classList.add("hidden");
      soundwave.classList.remove("active");
    }
  }

  if (isSpeaking) {
    window.speechSynthesis.cancel();
    resetSpeechUI();
    return;
  }

  const textToRead = textEl.textContent.trim();
  if (!textToRead) return;

  window.speechSynthesis.cancel();
  speechUtterance = new SpeechSynthesisUtterance(textToRead);

  // Set voice language
  const langMap = { en: "en-IN", hi: "hi-IN", mr: "mr-IN", pa: "pa-IN", gu: "gu-IN", ta: "ta-IN", te: "te-IN" };
  speechUtterance.lang = langMap[currentLang] || "en-IN";

  speechUtterance.onend = resetSpeechUI;
  speechUtterance.onerror = resetSpeechUI;

  window.speechSynthesis.speak(speechUtterance);
  isSpeaking = true;
  btn.innerHTML = `⏸️ <span id="lblSpeak">${t("ttsPlaying")}</span>`;
  if (soundwave) {
    soundwave.classList.remove("hidden");
    soundwave.classList.add("active");
  }
}

// ── DOWNLOAD CSV ──
function downloadCsv() {
  if (!currentResults || !currentResults.ranked) {
    showToast("No data to download", true);
    return;
  }

  const rows = currentResults.ranked;
  const headers = ["Rank", "Market", "District", "State", "Modal Price (Rs/q)", "Distance (km)", "Transport Cost (Rs/q)", "Net Price (Rs/q)", "Arrival Date", "Approximate Location"];
  const csvLines = [headers.join(",")];

  rows.forEach((r) => {
    const line = [
      r.rank,
      `"${(r.market || "").replace(/"/g, '""')}"`,
      `"${(r.district || "").replace(/"/g, '""')}"`,
      `"${(r.state || "").replace(/"/g, '""')}"`,
      r.modal_price,
      r.distance_km,
      r.transport_cost,
      r.net_price,
      `"${r.price_date || r.arrival_date || ""}"`,
      r.approximate_location ? "Yes" : "No",
    ];
    csvLines.push(line.join(","));
  });

  const blob = new Blob([csvLines.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `mandi_prices_${document.getElementById("cropValue")?.value || "crop"}_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast("CSV downloaded successfully");
}

// ── SPEECH-TO-TEXT (MIC BUTTON) ──
let mediaRecorder = null;
let audioChunks = [];

function setupMic() {
  const micBtn = document.getElementById("micBtn");
  if (!micBtn) return;

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    micBtn.classList.add("hidden");
    return;
  }

  micBtn.classList.remove("hidden");

  micBtn.addEventListener("click", async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      micBtn.classList.remove("recording");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "speech.webm");

        showToast("Transcribing crop voice input…");
        try {
          const res = await fetch(`/api/transcribe?lang=${encodeURIComponent(currentLang)}`, { method: "POST", body: formData });
          if (!res.ok) throw new Error("Whisper transcription unavailable");
          const data = await res.json();
          if (data.text) {
            const cleanText = data.text.trim();
            await applyVoiceFilter(cleanText);
          }
        } catch (err) {
          showToast("Speech transcription unavailable (Whisper not installed)", true);
        }
      };

      mediaRecorder.start();
      micBtn.classList.add("recording");
      showToast("Listening… speak crop name (e.g. Onion, Tamatar, Soybean)");
    } catch (err) {
      showToast("Microphone access denied", true);
    }
  });
}

// ── SMART VOICE FILTER MATCHER ──
const SPOKEN_CROP_SYNONYMS = {
  onion: "Onion",
  anian: "Onion",
  anion: "Onion",
  onions: "Onion",
  pyaz: "Onion",
  pyaaz: "Onion",
  kanda: "Onion",
  dungli: "Onion",
  dungri: "Onion",
  vengayam: "Onion",
  ullipaya: "Onion",
  tomato: "Tomato",
  tomatoes: "Tomato",
  tamatar: "Tomato",
  tometo: "Tomato",
  tameta: "Tomato",
  thakkali: "Tomato",
  potato: "Potato",
  potatoes: "Potato",
  aloo: "Potato",
  alu: "Potato",
  batata: "Potato",
  bataka: "Potato",
  urulaikizhangu: "Potato",
  wheat: "Wheat",
  gehu: "Wheat",
  gehun: "Wheat",
  gahu: "Wheat",
  kanak: "Wheat",
  ghau: "Wheat",
  rice: "Rice",
  paddy: "Rice",
  dhan: "Rice",
  chawal: "Rice",
  tandul: "Rice",
  jhona: "Rice",
  soybean: "Soybean",
  soyabean: "Soybean",
  soya: "Soybean",
  cotton: "Cotton",
  kapas: "Cotton",
  kapus: "Cotton",
  maize: "Maize",
  makka: "Maize",
  corn: "Maize",
  bhutta: "Maize",
  mustard: "Mustard",
  sarson: "Mustard",
  rai: "Mustard",
  garlic: "Garlic",
  lahsun: "Garlic",
  lasun: "Garlic",
  ginger: "Ginger",
  adrak: "Ginger",
  turmeric: "Turmeric",
  haldi: "Turmeric",
  chilli: "Chilli",
  chili: "Chilli",
  mirch: "Chilli",
  mirchi: "Chilli",
  gram: "Gram",
  chana: "Gram",
  chole: "Gram",
  harbhara: "Gram",
  apple: "Apple",
  seb: "Apple",
  banana: "Banana",
  kela: "Banana",
  mango: "Mango",
  aam: "Mango",
};

const SPOKEN_STATE_SYNONYMS = {
  gujarat: "Gujarat",
  gujarati: "Gujarat",
  maharashtra: "Maharashtra",
  marathi: "Maharashtra",
  punjab: "Punjab",
  punjabi: "Punjab",
  rajasthan: "Rajasthan",
  rajasthani: "Rajasthan",
  haryana: "Haryana",
  haryanvi: "Haryana",
  madhyapradesh: "Madhya Pradesh",
  "madhya pradesh": "Madhya Pradesh",
  mp: "Madhya Pradesh",
  uttarpradesh: "Uttar Pradesh",
  "uttar pradesh": "Uttar Pradesh",
  up: "Uttar Pradesh",
  karnataka: "Karnataka",
  kannada: "Karnataka",
  tamilnadu: "Tamil Nadu",
  "tamil nadu": "Tamil Nadu",
  tamil: "Tamil Nadu",
  andhrapradesh: "Andhra Pradesh",
  "andhra pradesh": "Andhra Pradesh",
  andhra: "Andhra Pradesh",
  telangana: "Telangana",
  telugu: "Telangana",
  bengal: "West Bengal",
  bengali: "West Bengal",
  westbengal: "West Bengal",
  "west bengal": "West Bengal",
  bihar: "Bihar",
  bihari: "Bihar",
  odisha: "Odisha",
  orissa: "Odisha",
  kerala: "Kerala",
  delhi: "Delhi",
  uttarakhand: "Uttarakhand",
  himachal: "Himachal Pradesh",
  assam: "Assam",
};

function levenshteinDist(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

async function applyVoiceFilter(rawText) {
  if (!rawText || !rawText.trim()) return;

  const normalized = rawText.toLowerCase().replace(/[^\w\s\u0900-\u0D7F]/gi, " ").replace(/\s+/g, " ").trim();
  const words = normalized.split(" ");

  // 1. Match Crop
  let matchedCrop = null;

  // Exact phrase check in known synonyms
  for (const [key, cropName] of Object.entries(SPOKEN_CROP_SYNONYMS)) {
    if (normalized.includes(key)) {
      matchedCrop = cropName;
      break;
    }
  }

  // Check appMeta.crops directly
  if (!matchedCrop && appMeta && appMeta.crops) {
    for (const crop of appMeta.crops) {
      if (normalized.includes(crop.toLowerCase())) {
        matchedCrop = crop;
        break;
      }
      const labels = CROP_LABELS[crop];
      if (labels) {
        for (const rWord of Object.values(labels)) {
          if (rWord && normalized.includes(rWord.toLowerCase())) {
            matchedCrop = crop;
            break;
          }
        }
      }
      if (matchedCrop) break;
    }
  }

  // Fuzzy word matching (allows 1 typo, e.g. "anian" -> "onion", "alloo" -> "aloo")
  if (!matchedCrop) {
    for (const w of words) {
      if (w.length < 3) continue;
      for (const [alias, crop] of Object.entries(SPOKEN_CROP_SYNONYMS)) {
        if (alias.length >= 3 && Math.abs(alias.length - w.length) <= 1) {
          if (levenshteinDist(w, alias) <= 1) {
            matchedCrop = crop;
            break;
          }
        }
      }
      if (matchedCrop) break;
    }
  }

  // 2. Match State & District if spoken
  let matchedState = null;
  for (const [alias, stateName] of Object.entries(SPOKEN_STATE_SYNONYMS)) {
    if (normalized.includes(alias)) {
      matchedState = stateName;
      break;
    }
  }

  if (!matchedState && appMeta && appMeta.states) {
    for (const st of appMeta.states) {
      if (normalized.includes(st.toLowerCase())) {
        matchedState = st;
        break;
      }
    }
  }

  let matchedDistrict = null;
  if (appMeta && appMeta.districts) {
    for (const d of appMeta.districts) {
      const dLower = d.district.toLowerCase();
      if (dLower.length > 3 && normalized.includes(dLower)) {
        matchedDistrict = d.district;
        matchedState = d.state;
        break;
      }
    }
  }

  // Apply State / District filter
  if (matchedState) {
    const stateSel = document.getElementById("stateSelect");
    if (stateSel) {
      stateSel.value = matchedState;
      onStateChanged();
    }
    if (matchedDistrict) {
      const distSel = document.getElementById("districtSelect");
      if (distSel) {
        distSel.value = matchedDistrict;
        await onDistrictChanged();
      }
    } else {
      // Resolve state centroid coordinates
      try {
        const res = await fetch(`/api/geocode?state=${encodeURIComponent(matchedState)}&district=${encodeURIComponent(matchedState)}`);
        if (res.ok) {
          const gData = await res.json();
          userCoords = {
            lat: gData.lat,
            lon: gData.lon,
            state: matchedState,
            district: null,
            isApprox: true,
            source: "manual",
          };
          const locStatus = document.getElementById("locStatus");
          if (locStatus) {
            locStatus.innerHTML = `<span class="loc-badge manual">📍 State: ${matchedState} (Centroid)</span>`;
          }
          if (leafletMap) {
            updateUserMarkerOnMap();
            leafletMap.setView([userCoords.lat, userCoords.lon], 7);
          }
        }
      } catch (e) {}
    }
  }

  // Apply Crop filter
  if (matchedCrop) {
    selectCrop(matchedCrop);
  } else {
    const input = document.getElementById("cropInput");
    if (input) {
      input.value = rawText;
      populateCropDropdown(rawText);
    }
  }

  // Auto-search and announce feedback
  const activeCrop = document.getElementById("cropValue")?.value;
  if (matchedCrop || activeCrop) {
    showToast(`Voice Filter: ${matchedCrop || activeCrop}${matchedState ? ` in ${matchedState}` : ""}`);
    await fetchBestMandis();
  } else {
    showToast(`Heard: "${rawText}" (no crop matched)`, true);
  }
}

// ── DARK MODE TOGGLE ──
function setupDarkMode() {
  const darkToggle = document.getElementById("darkToggle");
  const isDarkSaved = getSaved("ms_dark");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const shouldBeDark = isDarkSaved !== null ? isDarkSaved === "true" : prefersDark;
  document.documentElement.classList.toggle("dark", shouldBeDark);
  document.documentElement.setAttribute("data-theme", shouldBeDark ? "dark" : "light");
  if (darkToggle) darkToggle.textContent = shouldBeDark ? "☀️" : "🌙";

  darkToggle?.addEventListener("click", () => {
    document.documentElement.classList.add("theme-transitioning");
    const isDark = document.documentElement.classList.toggle("dark");
    document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
    setSaved("ms_dark", isDark ? "true" : "false");
    darkToggle.textContent = isDark ? "☀️" : "🌙";

    setTimeout(() => {
      document.documentElement.classList.remove("theme-transitioning");
    }, 350);

    if (priceChart && currentResults && currentResults.best) {
      loadPriceTrend(document.getElementById("cropValue").value, currentResults.best.market, currentChartDays);
    }
  });
}

// ── DOM READY INITIALIZATION ──
document.addEventListener("DOMContentLoaded", () => {
  // 1. Language selector buttons
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => applyLanguage(btn.dataset.lang));
  });

  // 2. Dark mode
  setupDarkMode();

  // 3. Sliders with subtle number bump
  const radiusSlider = document.getElementById("radiusSlider");
  const radiusVal = document.getElementById("radiusVal");
  radiusSlider?.addEventListener("input", (e) => {
    if (radiusVal) {
      radiusVal.textContent = `${e.target.value} km`;
      radiusVal.classList.add("bump");
      setTimeout(() => radiusVal.classList.remove("bump"), 180);
    }
  });

  const rateSlider = document.getElementById("rateSlider");
  const rateVal = document.getElementById("rateVal");
  rateSlider?.addEventListener("input", (e) => {
    if (rateVal) {
      rateVal.textContent = `₹${e.target.value}/q/km`;
      rateVal.classList.add("bump");
      setTimeout(() => rateVal.classList.remove("bump"), 180);
    }
  });

  // 4. Whole-state toggle
  const wholeStateToggle = document.getElementById("wholeStateToggle");
  wholeStateToggle?.addEventListener("change", (e) => {
    if (radiusSlider && radiusVal) {
      if (e.target.checked) {
        radiusSlider.value = "1500";
        radiusVal.textContent = "1500 km";
      } else {
        radiusSlider.value = "300";
        radiusVal.textContent = "300 km";
      }
      radiusVal.classList.add("bump");
      setTimeout(() => radiusVal.classList.remove("bump"), 180);
    }
  });

  // 5. Crop Input Autocomplete
  const cropInput = document.getElementById("cropInput");
  cropInput?.addEventListener("input", (e) => {
    populateCropDropdown(e.target.value);
  });
  cropInput?.addEventListener("focus", () => {
    populateCropDropdown(cropInput.value);
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-input-wrap") && !e.target.closest("#cropDropdown")) {
      document.getElementById("cropDropdown")?.classList.add("hidden");
    }
  });

  // 6. Location Controls
  document.getElementById("geoBtn")?.addEventListener("click", useGpsLocation);
  document.getElementById("stateSelect")?.addEventListener("change", onStateChanged);
  document.getElementById("districtSelect")?.addEventListener("change", onDistrictChanged);

  // 7. Search Buttons
  document.getElementById("searchBtn")?.addEventListener("click", fetchBestMandis);
  document.getElementById("mobileSearchBtn")?.addEventListener("click", fetchBestMandis);

  // 8. Error Retry Button
  document.getElementById("retryBtn")?.addEventListener("click", () => {
    if (lastFailingCall) {
      lastFailingCall();
    } else {
      loadAppMeta();
    }
  });

  // 9. Expand Radius Button
  document.getElementById("expandRadiusBtn")?.addEventListener("click", () => {
    if (radiusSlider && radiusVal) {
      radiusSlider.value = "1000";
      radiusVal.textContent = "1000 km";
      fetchBestMandis();
    }
  });

  // 10. Chart Tabs
  document.getElementById("tab30")?.addEventListener("click", () => {
    if (currentChartMarket) {
      loadPriceTrend(currentChartCrop || document.getElementById("cropValue")?.value, currentChartMarket, 30);
    }
  });
  document.getElementById("tab7")?.addEventListener("click", () => {
    if (currentChartMarket) {
      loadPriceTrend(currentChartCrop || document.getElementById("cropValue")?.value, currentChartMarket, 7);
    }
  });

  // 11. TTS & Download CSV
  document.getElementById("speakBtn")?.addEventListener("click", toggleSpeech);
  document.getElementById("downloadBtn")?.addEventListener("click", downloadCsv);
  document.getElementById("csvBtn")?.addEventListener("click", downloadCsv);

  // 12. Table sorting
  setupTableSorting();

  // 13. Microphone support
  setupMic();

  // 14. Initialize language
  const savedLang = getSaved("ms_lang", "en");
  applyLanguage(savedLang);

  // 15. Load initial metadata
  loadAppMeta();

  // 16. Button Ripple Animation
  document.querySelectorAll(".ripple-btn").forEach((button) => {
    button.addEventListener("click", function (e) {
      const rect = this.getBoundingClientRect();
      const circle = document.createElement("span");
      const diameter = Math.max(rect.width, rect.height);
      const radius = diameter / 2;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add("ripple");

      const existingRipple = this.querySelector(".ripple");
      if (existingRipple) existingRipple.remove();

      this.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  });
});
