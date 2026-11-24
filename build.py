#!/usr/bin/env python3
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engine'))
from engine import Site, fmt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
f = lambda n: fmt(n, ' ')

THEME = """
/* VOICE: measured French investment guide, factual and prudent
   IDEA: an investor's field notebook: Georgian vineyard hills, prices set out like a ledger
   PICTURE: terraced vineyard hills, a hilltop chapel and a village; price rows
   COLOUR and TYPE: white ground, terracotta dominant, pale peach support, deep blue accent; Poppins + Source Sans 3
   LAYOUT: full-width bands, 1240px content, square corners */
:root{color-scheme:light;--bg:#fff;--ink:#22160f;--ink2:#47352a;--mute:#6f5c50;--sea:#a63d2a;--sea2:#c24e37;--aqua:#fbf0ea;--line:#efdcd2;--line2:#dcc0b2;--coral:#1d4e89;
--tint1:#fbe9df;--tint2:#fffaf7;--radius:0;--btn-radius:0;--bar-radius:0;--head-font:Poppins,system-ui,sans-serif;--body-font:'Source Sans 3',system-ui,sans-serif;--head-weight:600;--foot-bg:#2a120b;--foot-ink:#f1ddd3}
body{font-size:17.5px}
"""

SRC = {
 'conv': ('Convention fiscale France–Géorgie du 7 mars 2007 (impots.gouv.fr)', 'https://WWW.impots.gouv.fr/sites/default/files/media/10_conventions/georgie/georgie_convention.pdf'),
 'bofip': ('BOFiP : convention fiscale entre la France et la Géorgie, entrée en vigueur', 'https://bofip.impots.gouv.fr/node/8273'),
 'an': ('Assemblée nationale : projet de loi sur la convention France–Géorgie (revenus immobiliers)', 'https://www.assemblee-nationale.fr/13/pdf/projets/pl1060.pdf'),
 'visa': ('Skyscanner : conditions d\'entrée en Géorgie pour les Français', 'https://www.skyscanner.fr/destinations/visa/29475247/georgie'),
 'visa2': ('Chapka : séjour sans visa jusqu\'à 365 jours', 'https://blog.chapkadirect.fr/assurance-voyage-obligatoire-pour-vos-vacances-en-georgie/'),
 'fl_tbs': ('Partir.com : vols directs Paris–Tbilissi', 'https://www.partir.com/Georgie/billet-avion-vol/paris-cdg-tbilissi/cdg/tbs/vol-direct.html'),
 'fl_tbs2': ('KAYAK : vols directs Paris–Tbilissi, durée', 'https://www.kayak.fr/vols/Paris-PAR/Aeroport-international-Shota-Rustaveli-de-Tbilissi-TBS'),
 'fl_kut': ('KAYAK : vols directs Paris Beauvais–Koutaïssi', 'https://www.kayak.fr/vols/Paris-PAR/Aeroport-international-David-IV-de-Koutaissi-KUT'),
 'fl_lyon': ('Carrefour Voyages : liaison Lyon–Koutaïssi', 'https://voyages.carrefour.fr/accueil/vol/georgie'),
 'gt_kob': ('Galt &amp; Taggart : huit mois 2026, nationalités des acheteurs à Batoumi (Homesoverseas)', 'https://www.homesoverseas.ru/eng/news/Bolee_70_kvartir_prodannyh_v_Batumi_v_2026_godu_priobreli_inostrancy'),
 'gt_sales': ('Galt &amp; Taggart : ventes à Batoumi, janvier–août 2026 (International Investment)', 'https://internationalinvestment.biz/en/business/9064-batumi-real-estate-market-sales-growth-galt-taggart.html'),
 'gt_aug': ('Galt &amp; Taggart : prix par quartier à Batoumi, janvier–août 2026 (International Investment)', 'https://internationalinvestment.biz/en/business/9099-batumi-real-estate-trends-prices-and-sales-by-district.html'),
 'oversupply': ('International Investment : marché de Batoumi, ventes et risque de suroffre', 'https://internationalinvestment.biz/en/real-estate/8149-batumi-housing-market-sales-growth-and-risks-of-oversupply.html'),
 'ii_2026': ('Prix et rendements à Tbilissi et Batoumi, 2026 (International Investment)', 'https://internationalinvestment.biz/en/real-estate/8910-georgia-real-estate-2026-prices-and-yields-in-tbilisi-and-batumi.html'),
 'tbc_sep': ('TBC Capital : Tbilissi, septembre 2026 (International Investment)', 'https://internationalinvestment.biz/en/real-estate/9034-tbilisi-apartment-sale-prices-september-tbc-capital.html'),
 'geostat_q3': ('Geostat : prix par district à Tbilissi, T3 2026 (Georgia Today)', 'https://georgiatoday.ge/?p=115443'),
 'hs_yield': ('Homesoverseas : rendement à Batoumi passé de 8,8 % à 7,1 %', 'https://www.homesoverseas.ru/eng/articles/14899'),
 'gpg_yield': ('Global Property Guide : rendements locatifs en Géorgie', 'https://www.globalpropertyguide.com/europe/georgia/rental-yields'),
 'gpg_hist': ('Global Property Guide : historique des prix et prévisions', 'https://www.globalpropertyguide.com/Asia/Georgia/Price-History'),
 'gpg_buy': ('Global Property Guide : frais d\'acquisition en Géorgie', 'https://www.globalpropertyguide.com/asia/georgia/buying-guide'),
 'madloba_buy': ('Madloba : achat immobilier par un étranger', 'https://madloba.info/en/faq/housing/buying-property-in-georgia-as-a-foreigner/'),
 'madloba_rent': ('Madloba : impôt sur la location (art. 81 du Code fiscal)', 'https://madloba.info/en/faq/work-business-taxes/tax-on-renting-out-an-apartment-in-georgia/'),
 'madloba_tax': ('Madloba : impôts et statut de petite entreprise', 'https://madloba.info/faq/work-business-taxes/taxes-and-vat-in-georgia/'),
 'madloba_poa': ('Madloba : procuration pour une transaction en Géorgie', 'https://madloba.info/en/blog/laws-of-georgia/doverennost-ne-grazhdaninu-gruzii'),
 'madloba_rp': ('Madloba : délais d\'examen du titre de séjour', 'https://madloba.info/en/faq/residence-and-citizenship/check-residence-permit-status-georgia/'),
 'chambers': ('Chambers Real Estate 2026 : Georgia', 'https://practiceguides.chambers.com/practice-guides/real-estate-2026/georgia'),
 'eig': ('EIG Law : seuil du titre de séjour immobilier au 1er mars 2026', 'https://eiglaw.com/georgia-to-increase-real-estate-investment-threshold-for-residence-permits-effective-march-1-2026/'),
 'visaatlas': ('VisaAtlas : séjour temporaire des propriétaires', 'https://visaatlas.org/visas/georgia/short-term-residence-real-estate'),
 'sda': ('Agence de développement des services publics : titres de séjour', 'https://sda.gov.ge/en/products/migration-residence-permits/'),
 'andersen': ('Andersen Georgia : impôt à la revente', 'https://ge.andersen.com/georgia-property-tax/'),
 'sova': ('SOVA : seuil de la taxe foncière relevé à 100 000 GEL', 'https://sovanews.tv/en/2026/09/30/georgian-parliament-approves-abolition-of-40000-gel-property-tax-threshold/amp/'),
 'safebuy': ('SafeBuy : vérifier un programme neuf au registre', 'https://safebuy.ge/properties/new-developments'),
 'korter_frames': ('Korter : carcasse noire, blanche et verte', 'https://korter.ge/en/new-projects-tbilisi-black-frame'),
 'napr': ('Agence nationale du registre public', 'https://napr.gov.ge'),
 'rs': ('Service des impôts de Géorgie', 'https://www.rs.ge'),
}

S = Site(domain='https://investir-georgie.com', lang='fr', out=OUT, utm='investir-georgie', theme_css=THEME,
         fonts_href='https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap',
         logo='Investir<span> en </span>Géorgie',
         nav=[('', 'Accueil'), ('batumi/', 'Batoumi'), ('tbilissi/', 'Tbilissi'), ('acheter/', 'Acheter'), ('fiscalite/', 'Fiscalité'),
              ('rendement/', 'Rendement'), ('residence/', 'Titre de séjour'), ('voyager/', 'Vols et séjour'), ('faq/', 'FAQ')],
         labels=dict(home='Accueil', updated='Mis à jour', sources='Sources', crumbs='Fil d\'Ariane', nav='Rubriques', facts_label='Chiffres clés',
                     sources_note='Chaque chiffre indique sa période et sa source. Les analystes mesurent des segments différents : ne comparez que des chiffres d\'une même source.',
                     draft='Brouillon à valider. Les annonces d\'exemple seront remplacées ; tous les autres chiffres sont sourcés.',
                     disclaimer='Information générale, et non conseil juridique ou fiscal.',
                     submit='Envoyer la demande', form_draft='Brouillon : le formulaire n\'est pas encore connecté, rien n\'a été envoyé.'),
         footer_blurb='<b>Investir en Géorgie</b> est un guide en français pour investir dans l\'immobilier géorgien, projet <a href="{BRIK}">Brik</a>.',
         footer_cols=[('Villes', [('batumi/', 'Batoumi'), ('tbilissi/', 'Tbilissi')]),
                      ('Investir', [('acheter/', 'Acheter'), ('fiscalite/', 'Fiscalité'), ('rendement/', 'Rendement'), ('residence/', 'Titre de séjour')]),
                      ('Le guide', [('voyager/', 'Vols et séjour'), ('faq/', 'FAQ'), ('a-propos/', 'À propos'), ('contact/', 'Contact'), ('confidentialite/', 'Confidentialité')])],
         updated='novembre 2026', sources=SRC)

BAT = [('Vieux Batoumi', 3224, 839), ('Gonio–Kvariati', 2657, 196), ('Allée des Héros', 2255, 2485), ('Makhindjaouri', 1998, 779), ('Nouveau Boulevard', 1798, 4417), ('Kobouleti', 1734, 401)]
TBS = [('Vaké', 3180), ('Saburtalo', 1732), ('Krtsanissi', 1671), ('Didoubé', 1425), ('Issani', 1407), ('Samgori', 1178), ('Didi Digomi', 1148), ('Gldani', 1146)]

SCENE = '''<svg class="scene" viewBox="0 0 600 500" role="img" aria-label="Illustration : collines de vignes en Géorgie, une chapelle sur la crête et un village">
<defs><linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe3d6"/><stop offset="1" stop-color="#fffaf7"/></linearGradient>
<linearGradient id="fh1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c98a6b"/><stop offset="1" stop-color="#a86a4d"/></linearGradient>
<linearGradient id="fh2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8a4a"/><stop offset="1" stop-color="#5e6a35"/></linearGradient></defs>
<rect width="600" height="500" fill="url(#fsky)"/>
<circle cx="470" cy="100" r="40" fill="#f4b183"/>
<path d="M0 240 C90 190 190 170 280 200 C370 230 470 170 600 200 V320 H0Z" fill="#e4c3b0"/>
<path d="M0 300 C120 230 250 220 360 260 C450 292 530 270 600 250 V380 H0Z" fill="url(#fh1)"/>
<g transform="translate(300 214)"><rect x="-14" y="-30" width="28" height="30" fill="#fff"/><path d="M-18 -30 L0 -50 L18 -30Z" fill="#a63d2a"/><rect x="-3" y="-64" width="6" height="16" fill="#a63d2a"/><rect x="-4" y="-18" width="8" height="18" fill="#a63d2a" opacity=".6"/></g>
<path d="M0 360 C130 320 260 320 380 350 C470 372 540 360 600 344 V500 H0Z" fill="url(#fh2)"/>
<g stroke="#3f4a1f" stroke-width="3" stroke-linecap="round" opacity=".55" fill="none">
 <path d="M20 400 C140 368 260 368 380 392 C460 408 530 400 590 388"/><path d="M10 430 C140 398 270 398 390 422 C470 438 540 430 600 418"/><path d="M0 460 C140 428 280 428 400 452 C480 468 550 460 600 450"/><path d="M0 490 C150 458 290 458 410 482 C490 498 560 490 600 480"/></g>
<g fill="#fff"><rect x="460" y="300" width="30" height="26"/><rect x="496" y="292" width="24" height="34"/><rect x="524" y="304" width="30" height="22"/></g>
<g fill="#a63d2a"><path d="M456 302 l19 -14 l19 14Z"/><path d="M492 294 l16 -14 l16 14Z"/><path d="M520 306 l19 -14 l19 14Z"/></g>
</svg>'''

def form(extra=''):
    return S.lead_form(f'''<label>Nom<input name="name" autocomplete="name" required></label>
<label>WhatsApp, Telegram ou e-mail<input name="contact" required></label>
<label>Ville<select name="city"><option>Je ne sais pas encore</option><option>Batoumi</option><option>Tbilissi</option><option>Autre ville de Géorgie</option></select></label>
<label>Budget<select name="budget"><option>Moins de 80 000 $</option><option>80 000–150 000 $</option><option>150 000–300 000 $</option><option>Plus de 300 000 $</option></select></label>
<label>Objectif<select name="goal"><option>Investissement locatif</option><option>Résidence secondaire</option><option>Titre de séjour</option><option>M\'installer en Géorgie</option></select></label>{extra}''')

CTA = lambda c, t='Les biens en Géorgie sur Brik', x='Annonces de promoteurs, d\'agences et de particuliers, filtrables par ville, prix et surface.': S.cta(c, t, x, 'Voir les annonces')
usd = lambda n: f'{f(n)} $'

S.page('', 'Investir dans l\'immobilier en Géorgie — guide en français',
 'Guide en français pour investir dans l\'immobilier en Géorgie : prix à Batoumi et Tbilissi, achat par un étranger, fiscalité et convention France–Géorgie, rendement locatif, titre de séjour.', None, f'''
<section class="hero band"><div class="wrap">
 <div><h1>Investir dans l'immobilier en Géorgie : prix, règles et rendements</h1>
 <p class="lede">Un Français peut acheter un appartement en Géorgie aux mêmes conditions qu'un Géorgien, sans visa ni titre de séjour. Les prix restent bas par rapport à l'Europe, mais le rendement réel dépend beaucoup de la ville, du bien et de sa gestion.</p>
 <div class="ctas"><a class="btn" href="#villes">Batoumi ou Tbilissi ?</a>{S.a("acheter/", "Comment acheter", "btn ghost")}</div></div>
 {SCENE}
</div></section>
{S.facts([('1 373 $', 'prix moyen au m² à Tbilissi', 'septembre 2026, TBC Capital'), ('1 408 $', 'prix moyen au m² dans le neuf à Batoumi', 'septembre 2026, Colliers'), ('7,1–8,3 %', 'rendement locatif brut, Batoumi et Tbilissi', '2026, Galt &amp; Taggart, TBC Capital'), ('365 jours', 'de séjour sans visa pour les Français', 'conditions d\'entrée 2026')])}
<section class="band" id="villes"><div class="wrap two">
 <a class="dcard" href="@/batumi/index.html"><b>Batoumi</b><span class="p">station balnéaire</span><p>Marché porté par les acheteurs étrangers, dont 17 % d'Européens entre janvier et août 2026. Beaucoup de location saisonnière, mais une offre abondante.</p></a>
 <a class="dcard" href="@/tbilissi/index.html"><b>Tbilissi</b><span class="p">capitale</span><p>Marché surtout local, location à l'année, rendement brut d'environ 8,3 %. Écarts de prix importants entre quartiers.</p></a>
</div></section>
<section class="band alt"><div class="wrap two">
 <div><h2>Les points forts</h2><ul class="txt"><li>Achat simple : un passeport suffit, enregistrement en un à quelques jours ouvrés.</li><li>Pas de droits de mutation, frais d'acquisition de 0,6 à 1,1 % du prix.</li><li>Convention fiscale France–Géorgie depuis 2011.</li><li>Vols directs Paris–Tbilissi et Paris–Koutaïssi.</li></ul></div>
 <div><h2>Les points de vigilance</h2><ul class="txt"><li>Prix et loyers en dollars, coûts en lari : risque de change.</li><li>À Batoumi, forte offre de studios similaires et saisonnalité.</li><li>Pas de garantie publique pour l'achat sur plan.</li><li>Les revenus restent à déclarer en France.</li></ul></div>
</div></section>
<section class="band" id="lead"><div class="wrap two">
 <div><h2>Recevoir une sélection</h2><p>Indiquez votre budget et votre objectif : un agent Brik vous enverra des biens adaptés. Votre demande n'est transmise qu'à l'équipe Brik ; voir la {S.a("confidentialite/", "politique de confidentialité")}.</p>
 <p class="sub">Contenu relu par les partenaires de Brik en Géorgie. {S.a("a-propos/", "À propos")}</p></div>
 {form()}
</div></section>''', srcs=['madloba_buy', 'tbc_sep', 'ii_2026', 'gt_kob', 'gpg_buy', 'conv', 'bofip', 'visa', 'fl_tbs', 'fl_kut'])

S.page('batumi/', 'Immobilier à Batoumi — prix par quartier et rendement',
 'Acheter un appartement à Batoumi : prix au m² par quartier, profil des acheteurs, rendement locatif, saisonnalité et points à vérifier sur un programme neuf.',
 [('batumi/', 'Batoumi')], f'''
<section class="band"><div class="wrap"><h2>Prix au m² par quartier</h2><p>Appartements finis du marché primaire, janvier–août 2026, Galt &amp; Taggart.</p>
 {S.rows([(n, f'{f(s)} ventes', p, usd(p) + '/m²', None) for n, p, s in BAT], 3300)}</div></section>
<section class="band alt"><div class="wrap two">
 <div class="prose"><h2>Qui achète à Batoumi</h2><p>Chez les promoteurs interrogés par Galt &amp; Taggart sur janvier–août 2026, les Géorgiens représentent 28 % des achats. Viennent ensuite les acheteurs d'Ukraine, de Russie et de Biélorussie (19 %), d'Europe (17 %) et d'Israël (12 %).</p>
 <h2>Les quartiers en bref</h2><ul class="txt"><li><b>Nouveau Boulevard</b> : la plupart des tours et apart-hôtels récents, environ 40 % des ventes de la ville.</li><li><b>Vieux Batoumi</b> : le centre historique, le plus cher.</li><li><b>Makhindjaouri, Gonio–Kvariati</b> : quartiers plus calmes au nord et au sud.</li><li><b>Kobouleti</b> : station distincte au nord, moins chère.</li></ul></div>
 <div class="prose"><h2>Rendement et risques</h2><p>Le rendement brut est d'environ 7,1 % (juin 2026, Galt &amp; Taggart), contre 8,8 % en 2024. Galt &amp; Taggart signale un important volume d'apart-hôtels en construction, qui peut peser sur les loyers.</p>
 <ul class="check"><li>Le promoteur est propriétaire du terrain, non hypothéqué.</li><li>Le permis de construire correspond au projet.</li><li>Le lot est enregistré comme logement, et non comme chambre d'hôtel.</li><li>Les paiements suivent l'avancement des travaux.</li></ul></div>
</div></section>
{CTA('batumi', 'Appartements à Batoumi', 'Une sélection de biens à Batoumi sur Brik.')}''', h1='Immobilier à Batoumi',
 lede='À Batoumi, 72 % des acheteurs des programmes neufs étudiés étaient étrangers entre janvier et août 2026. Un appartement fini neuf coûte de 1 734 $ à 3 224 $ le m² selon le quartier.',
 srcs=['gt_aug', 'gt_kob', 'gt_sales', 'ii_2026', 'hs_yield', 'oversupply', 'safebuy'])

S.page('tbilissi/', 'Immobilier à Tbilissi — quartiers, prix et rendement',
 'Acheter un appartement à Tbilissi : prix au m² par quartier, rendement locatif, ancien soviétique ou neuf, profil du marché.',
 [('tbilissi/', 'Tbilissi')], f'''
<section class="band"><div class="wrap"><h2>Prix au m² du neuf par quartier</h2><p>TBC Capital, juillet 2026, carcasse blanche.</p>
 {S.rows([(n, 'logements neufs', p, usd(p) + '/m²', None) for n, p in TBS], 3300)}
 <p class="sub" style="margin-top:12px">Mtatsminda, centre historique, est le plus cher selon Geostat (7 004 GEL le m², T3 2026), mais TBC Capital n'y publie pas de prix en dollars.</p></div></section>
<section class="band alt"><div class="wrap two">
 <div class="prose"><h2>Le marché en bref</h2><ul class="txt"><li>Prix moyen : 1 373 $ le m² en septembre 2026 (TBC Capital).</li><li>Rendement brut : 8,3 % en août 2026.</li><li>Acheteurs étrangers : environ 12 % des transactions.</li></ul><p>Contrairement à Batoumi, Tbilissi est un marché d'acheteurs locaux et de location à l'année.</p></div>
 <div class="prose"><h2>Ancien ou neuf</h2><p>Une grande partie du marché de seconde main se trouve dans des immeubles d'époque soviétique : faites vérifier la structure et les réseaux par un ingénieur. Le neuf se vend en carcasse noire, blanche ou verte, ou fini. Le contenu de chaque niveau dépend du promoteur.</p></div>
</div></section>
{CTA('tbilisi', 'Appartements à Tbilissi', 'Une sélection de biens à Tbilissi sur Brik.')}''', h1='Immobilier à Tbilissi',
 lede='Le m² valait en moyenne 1 373 $ à Tbilissi en septembre 2026. Dans le neuf, les prix vont de 1 146 $ à Gldani à 3 180 $ à Vaké.',
 srcs=['ii_2026', 'tbc_sep', 'geostat_q3', 'korter_frames'])

S.page('acheter/', 'Acheter un bien en Géorgie quand on est français — étapes',
 'Les étapes pour acheter un appartement en Géorgie : vérification au registre, compromis, paiement bancaire, acte, enregistrement, achat sur plan et achat à distance.',
 [('acheter/', 'Acheter')], f'''
<section class="band"><div class="wrap"><h2>Les étapes</h2>
 <ol class="steps">
  <li><h3>Choisir</h3><p>Ville, quartier, neuf ou ancien, et objectif : location, résidence secondaire ou titre de séjour.</p></li>
  <li><h3>Vérifier au registre</h3><p>Extrait de l'Agence nationale du registre public (napr.gov.ge) : propriétaire, hypothèque, saisie.</p></li>
  <li><h3>Avant-contrat</h3><p>Prix, délais, acompte et conditions de remboursement. Faites-le relire par un avocat.</p></li>
  <li><h3>Paiement bancaire</h3><p>Virement sur le compte du vendeur. La banque peut demander l'origine des fonds.</p></li>
  <li><h3>Acte de vente</h3><p>Signé chez un notaire ou à la Maison de la justice, en géorgien, souvent avec traduction.</p></li>
  <li><h3>Enregistrement</h3><p>La propriété est transférée lors de l'inscription au registre public, en général en un à quelques jours ouvrés.</p></li>
 </ol></div></section>
<section class="band alt"><div class="wrap two">
 <div class="prose"><h2>Qui peut acheter</h2><p>Les étrangers, personnes physiques ou sociétés, achètent appartements, maisons et locaux commerciaux comme les Géorgiens. Seules les terres agricoles sont réservées. Ni visa, ni titre de séjour, ni associé local ne sont nécessaires.</p>
 <h2>Acheter à distance</h2><p>Un mandataire peut signer pour vous avec une procuration notariée, apostillée en France puis traduite en géorgien et certifiée en Géorgie.</p></div>
 <div class="prose"><h2>Acheter sur plan</h2><p>Il n'existe pas de garantie publique protégeant les fonds des acheteurs sur plan en Géorgie. Votre protection repose sur le contrat, l'échéancier et le sérieux du promoteur.</p>
 <ul class="check"><li>Terrain détenu par le promoteur et non hypothéqué.</li><li>Permis de construire pour cet immeuble.</li><li>Immeubles déjà livrés.</li><li>Date de livraison, pénalités de retard, remboursement.</li></ul></div>
</div></section>
{CTA('acheter')}''', h1='Acheter en Géorgie',
 lede='Un passeport suffit pour acheter en Géorgie. La vente est inscrite au registre public, en général en un à quelques jours ouvrés, et vous devenez propriétaire à ce moment-là.',
 srcs=['madloba_buy', 'chambers', 'madloba_poa', 'safebuy', 'napr'])

S.page('fiscalite/', 'Fiscalité de l\'immobilier en Géorgie pour un résident français',
 'Impôts sur un bien en Géorgie en 2026 : pas de droits de mutation, 5 % sur les loyers, taxe foncière au-delà de 100 000 GEL, plus-value, et convention fiscale France–Géorgie.',
 [('fiscalite/', 'Fiscalité')], f'''
<section class="band"><div class="wrap"><h2>En Géorgie</h2>
 <table class="stack"><thead><tr><th>Situation</th><th>Taux</th><th>Conditions</th></tr></thead><tbody>
 <tr><td>Achat</td><td class="k">pas de taxe</td><td>Pas de droits de mutation ; frais de l'acheteur d'environ 0,6 à 1,1 % du prix.</td></tr>
 <tr><td>Taxe foncière</td><td class="k">0 % ou 0,8–1 %</td><td>Depuis le 1er octobre 2026, due seulement si le revenu familial de l'année précédente dépasse 100 000 GEL ; sur la valeur de marché.</td></tr>
 <tr><td>Location d'habitation</td><td class="k">5 %</td><td>Sur les loyers bruts, sans déduction de charges (art. 81 du Code fiscal).</td></tr>
 <tr><td>Micro-entreprise</td><td class="k">1 % du CA</td><td>Statut de petite entreprise, chiffre d'affaires jusqu'à 500 000 GEL par an ; à valider pour la location courte.</td></tr>
 <tr><td>Revente après 2 ans</td><td class="k">0 %</td><td>Plus-value exonérée pour un logement détenu plus de deux ans.</td></tr>
 <tr><td>Revente avant 2 ans</td><td class="k">5 %</td><td>Sur la plus-value, pour un appartement.</td></tr>
 </tbody></table></div></section>
<section class="band alt"><div class="wrap two">
 <div class="prose"><h2>Et en France ?</h2><p>La France et la Géorgie ont signé à Paris, le 7 mars 2007, une convention pour éviter les doubles impositions. Elle s'applique aux revenus perçus depuis le 1er janvier 2011.</p>
 <p>Conformément au modèle de l'OCDE, les revenus d'un bien immobilier sont imposables dans l'État où il est situé. La France élimine ensuite la double imposition par un crédit d'impôt, selon les règles de la convention.</p></div>
 <div class="prose"><div class="note">Un résident fiscal français doit en principe déclarer en France ses revenus de source étrangère et ses comptes bancaires détenus à l'étranger. Avant d'acheter, faites valider le traitement des loyers et de la plus-value par un conseiller fiscal.</div>
 {S.related([('rendement/', 'Rendement'), ('acheter/', 'Acheter')])}</div>
</div></section>
{CTA('fiscalite')}''', h1='Fiscalité',
 lede='En Géorgie, pas de droits de mutation et 5 % d\'impôt sur les loyers d\'habitation. La convention France–Géorgie évite la double imposition, mais les revenus restent à déclarer en France.',
 srcs=['gpg_buy', 'ii_2026', 'sova', 'madloba_rent', 'madloba_tax', 'andersen', 'conv', 'bofip', 'an', 'rs'])

S.page('rendement/', 'Rendement locatif en Géorgie — Batoumi et Tbilissi',
 'Rendement locatif brut en Géorgie en 2026 : 8,3 % à Tbilissi, 7,1 % à Batoumi. Location courte, exemple de calcul, contrat de gestion d\'apart-hôtel.',
 [('rendement/', 'Rendement')], f'''
<section class="band"><div class="wrap"><h2>Rendement brut</h2>
 {S.rows([('Tbilissi', 'août 2026, TBC Capital', 8.3, '8,3 %', None), ('Moyenne Géorgie', 'T1 2026, Global Property Guide', 7.42, '7,42 %', None), ('Batoumi', 'juin 2026, Galt &amp; Taggart', 7.1, '7,1 %', None)], 9)}
 <p style="margin-top:14px">Le rendement net est en général inférieur de 1,5 à 2 points au rendement brut.</p></div></section>
<section class="band alt"><div class="wrap two">
 <div class="prose"><h2>Exemple de calcul</h2><p>Un 40 m² à Batoumi, loué entre 10,6 et 12,3 $ le m² par mois, rapporte environ 424 à 492 $ par mois, soit 5 100 à 5 900 $ par an avant charges. Après l'impôt de 5 %, la gestion, l'entretien et la vacance, le revenu net est nettement plus bas, et la fiscalité française s'applique ensuite.</p></div>
 <div class="prose"><h2>Location courte</h2><p>À Batoumi, la nuitée moyenne est d'environ 65 $ en haute saison et 54 $ en basse saison. À Tbilissi : 57 $ pour un taux d'occupation de 38,9 %.</p>
 <h2>Contrat de gestion</h2><p>Vérifiez la part de l'exploitant, qui paie entretien et mobilier, la durée du contrat et la sortie. Un rendement « garanti » par un promoteur est le plus souvent une projection.</p></div>
</div></section>
{CTA('rendement')}''', h1='Rendement locatif',
 lede='Le rendement brut atteint environ 8,3 % à Tbilissi et 7,1 % à Batoumi en 2026. C\'est avant impôts, gestion et vacance locative : le rendement réel est plus bas.',
 srcs=['ii_2026', 'gpg_yield', 'hs_yield', 'madloba_rent'])

S.page('residence/', 'Titre de séjour en Géorgie par l\'immobilier — 150 000 $',
 'Le titre de séjour géorgien pour les propriétaires depuis le 1er mars 2026 : seuil de 150 000 $, expertise, famille, délais, et surface nécessaire à Batoumi.',
 [('residence/', 'Titre de séjour')], f'''
{S.facts([('150 000 $', 'valeur de marché minimale d\'un bien non agricole', 'depuis le 1er mars 2026 ; 100 000 $ avant'), ('1 an', 'durée, renouvelable chaque année', 'EIG Law'), ('jusqu\'à 30 jours', 'délai d\'examen, plus court moyennant supplément', 'Madloba, octobre 2026')], three=True)}
<section class="band"><div class="wrap two">
 <div class="prose"><h2>Conditions</h2><ul class="txt"><li>Être propriétaire d'un bien non agricole en Géorgie, inscrit au registre public.</li><li>Valeur de marché d'au moins 150 000 $, établie par un expert agréé ; le prix de l'acte ne compte pas. Plusieurs biens peuvent être additionnés.</li><li>Le conjoint et les enfants peuvent être inclus.</li></ul>
 <p>Le titre n'est pas automatique : l'Agence de développement des services publics décide.</p></div>
 <div class="prose"><h2>À savoir</h2><ul class="txt"><li>Ce titre temporaire ne mène pas à la résidence permanente.</li><li>Les Français peuvent déjà séjourner jusqu'à 365 jours sans visa ; le titre sert surtout à s'installer durablement.</li><li>Le titre de séjour d'investisseur, distinct, exige au moins 300 000 $.</li></ul></div>
</div></section>
<section class="band alt"><div class="wrap"><h2>Surface nécessaire à Batoumi</h2><p>Au prix moyen de chaque quartier (Galt &amp; Taggart, janvier–août 2026). L'expertise du bien lui-même fait foi.</p>
 <table><thead><tr><th>Quartier</th><th class="n">$/m²</th><th class="n">Surface</th></tr></thead><tbody>{''.join(f'<tr><td>{n}</td><td class="n">{f(p)}</td><td class="n">{-(-150000 // p)} m²</td></tr>' for n, p, _ in BAT)}</tbody></table></div></section>
{CTA('residence', 'Biens à partir de 150 000 $', 'Des biens dont la valeur peut ouvrir droit au titre de séjour.')}''', h1='Titre de séjour par l\'immobilier',
 lede='Depuis le 1er mars 2026, un propriétaire d\'un bien en Géorgie valant au moins 150 000 $ peut demander un titre de séjour d\'un an, renouvelable.',
 srcs=['eig', 'madloba_rp', 'visaatlas', 'sda', 'visa', 'gt_aug', 'gt_kob'])

S.page('voyager/', 'Aller en Géorgie depuis la France — vols et séjour sans visa',
 'Vols directs Paris–Tbilissi et Paris–Koutaïssi, durée de vol, séjour sans visa jusqu\'à 365 jours pour les Français et assurance santé.',
 [('voyager/', 'Vols et séjour')], f'''
<section class="band"><div class="wrap two">
 <div class="prose"><h2>Vols directs</h2><ul class="txt"><li><b>Paris–Tbilissi</b> : vols directs d'Air France, Georgian Airways et Transavia, environ 4 h 35, quelques vols par semaine.</li><li><b>Paris Beauvais–Koutaïssi</b> : Wizz Air, environ 4 h 30.</li><li><b>Lyon–Koutaïssi</b> : Wizz Air.</li><li><b>Batoumi</b> : en général avec une escale depuis la France.</li></ul><p class="sub">Les programmes varient selon la saison : vérifiez auprès des compagnies.</p></div>
 <div class="prose"><h2>Entrée et séjour</h2><ul class="txt"><li>Les ressortissants français entrent sans visa et peuvent rester jusqu'à 365 jours.</li><li>Les citoyens de l'UE peuvent voyager avec une carte d'identité sécurisée en cours de validité.</li><li>Une assurance santé voyage est exigée pour entrer en Géorgie : vérifiez les conditions avant le départ.</li><li>Acheter un bien ne demande ni visa ni titre de séjour.</li></ul></div>
</div></section>
{CTA('voyager')}''', h1='Vols et séjour',
 lede='Tbilissi est à environ 4 h 30 de Paris en vol direct, et Koutaïssi est desservie par des vols à bas prix. Les Français peuvent séjourner en Géorgie jusqu\'à 365 jours sans visa.',
 srcs=['fl_tbs', 'fl_tbs2', 'fl_kut', 'fl_lyon', 'visa', 'visa2'])

FAQ = [
 ('Un Français peut-il acheter en Géorgie ?', 'Oui, aux mêmes conditions qu\'un Géorgien. Seules les terres agricoles sont réservées.', 'acheter/'),
 ('Faut-il un visa ?', 'Non : séjour sans visa jusqu\'à 365 jours, et l\'achat ne demande qu\'un passeport.', 'voyager/'),
 ('Combien coûte un appartement à Batoumi ?', 'Le neuf valait en moyenne 1 408 $ le m² en septembre 2026 ; un appartement fini neuf coûte de 1 734 à 3 224 $ le m² selon le quartier.', 'batumi/'),
 ('Quel rendement espérer ?', 'Environ 8,3 % brut à Tbilissi et 7,1 % à Batoumi en 2026, avant charges et impôts.', 'rendement/'),
 ('Y a-t-il une double imposition ?', 'La convention France–Géorgie de 2007 l\'évite, mais les revenus doivent être déclarés en France. Faites valider votre situation par un conseiller.', 'fiscalite/'),
 ('L\'achat donne-t-il un titre de séjour ?', 'Un bien d\'au moins 150 000 $ permet de demander un titre d\'un an. Il n\'est pas automatique.', 'residence/'),
 ('Peut-on acheter à distance ?', 'Oui, par procuration notariée apostillée, traduite en géorgien.', 'acheter/'),
]
ldq = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a, _ in FAQ]}, ensure_ascii=False)
S.page('faq/', 'Questions fréquentes — investir en Géorgie', 'Réponses courtes pour investir dans l\'immobilier en Géorgie depuis la France.', [('faq/', 'FAQ')],
 '<section class="band"><div class="wrap">' + ''.join(f'<details><summary>{q}</summary><p>{a} {S.a(t, "En savoir plus")}</p></details>' for q, a, t in FAQ) + '</div></section>' + CTA('faq'),
 h1='Questions fréquentes', lede='Réponses courtes et liens vers les pages détaillées. Données de novembre 2026.', srcs=['madloba_buy', 'visa', 'ii_2026', 'conv', 'eig'],
 head_extra=f'\n<script type="application/ld+json">{ldq}</script>')

S.page('a-propos/', 'À propos — Investir en Géorgie', 'Qui rédige ce guide, d\'où viennent les données et le lien avec Brik.', [('a-propos/', 'À propos')], f'''
<section class="band"><div class="wrap two"><div class="prose"><h2>Le guide</h2><p>Investir en Géorgie est un guide en français pour celles et ceux qui envisagent d'acheter un bien en Géorgie, surtout à Batoumi et Tbilissi.</p>
<p>Le site fait partie de <a href="{S.brik('about')}">Brik</a>, plateforme immobilière en Géorgie. Les liens vers les annonces et le formulaire mènent au catalogue et à l'agence Brik.</p>
<h2>Notre méthode</h2><ul class="txt"><li>Chaque chiffre indique sa source et sa période.</li><li>Pas de mélange de séries de prix d'analystes différents.</li><li>Les pages juridiques et fiscales sont relues par les partenaires de Brik en Géorgie.</li></ul></div>
<div class="prose"><h2>Auteurs</h2><div class="note">Brouillon : noms, photos et expérience des auteurs et relecteurs à ajouter.</div><h2>Une erreur ?</h2><p>Signalez-la via la {S.a("contact/", "page contact")}.</p></div></div></section>''',
 h1='À propos', lede='Un guide en français pour investir dans l\'immobilier géorgien, projet Brik.')

S.page('contact/', 'Contact — Investir en Géorgie', 'Contacter l\'équipe Brik pour un achat immobilier en Géorgie.', [('contact/', 'Contact')], f'''
<section class="band"><div class="wrap two"><div class="prose"><h2>Écrivez-nous</h2><p>Un agent Brik répond à vos questions sur les villes, les biens et la procédure, et vous envoie une sélection.</p><div class="note">Brouillon : téléphone, messageries, e-mail et adresse seront ajoutés avant le lancement.</div></div>
{form('<label>Votre question<textarea name="question"></textarea></label>')}</div></section>''', h1='Contact', lede='Posez une question ou demandez une sélection de biens.')

S.page('confidentialite/', 'Politique de confidentialité — Investir en Géorgie', 'Quelles données le site collecte et comment elles sont utilisées.', [('confidentialite/', 'Confidentialité')], '''
<section class="band"><div class="wrap prose"><div class="note">Brouillon pour relecture juridique : entité, adresse et contact pour les demandes RGPD à ajouter avant le lancement.</div>
<h2>Données collectées</h2><p>Ce que vous saisissez dans le formulaire : nom, coordonnées, ville, budget, objectif et message.</p>
<h2>Finalité</h2><p>Permettre à un agent Brik de vous contacter et de vous envoyer des biens adaptés. Aucun autre usage sans votre accord.</p>
<h2>Destinataires</h2><p>L'équipe Brik uniquement. Nous ne vendons pas vos données et ne les transmettons pas à des tiers, sauf obligation légale.</p>
<h2>Durée de conservation</h2><p>Le temps nécessaire pour vous répondre et accompagner votre projet, ou jusqu'à votre demande de suppression.</p>
<h2>Vos droits</h2><p>Vous pouvez demander l'accès à vos données, leur rectification ou leur suppression.</p>
<h2>Mesure d'audience</h2><p>Nous pouvons utiliser un outil de mesure d'audience. Les liens vers Brik portent des paramètres indiquant que la visite vient de ce site.</p></div></section>''',
 h1='Politique de confidentialité', lede='Comment nous traitons les données envoyées via le formulaire.')

S.finish()
