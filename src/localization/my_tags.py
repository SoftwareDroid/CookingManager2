from src.app.share.tag_manager import TagManager, DataType


# TODO if there is a circle  between parent and child tags there could be a endless recursion

def tags_init():
    # Time is comparable with a number
    TagManager.create_tag("duration", data_type=DataType.DURATION, search_shortcut="d",
                          display_name="Duration", default_value="1 h", render_priority=10, data_type_args={})

    TagManager.create_tag("rating", data_type=DataType.NUMBER, search_shortcut="r",
                          display_name="Rating", default_value="-1", render_priority=20,
                          data_type_args={"min": 1, "max": 5, "inc": 1, "digits": 0})
    #TagManager.create_tag("cuisine", data_type=DataType.STRING, search_shortcut="c",
    #                      display_name="Cuisine", default_value="N.A.", render_priority=30)
    TagManager.create_tag("need_grill", data_type=DataType.BOOL, display_name="Need Grill",
                          default_value=False, render_priority=200)
    TagManager.create_tag("vegetarian", data_type=DataType.BOOL,  display_name="Vegetarian",
                          default_value=False, render_priority=60,data_type_args={})
    TagManager.create_tag("author", data_type=DataType.STRING,  display_name="Author",
                          default_value="N.A.", render_priority=70)
    TagManager.create_tag("source", data_type=DataType.STRING,  display_name="Source",
                          default_value="N.A.", render_priority=80)

    TagManager.create_tag("portions", data_type=DataType.NUMBER, search_shortcut="p",
                          display_name="Portions", default_value="0", render_priority=35,
                          data_type_args={"min": 0, "max": 99, "inc": 1, "digits": 0})

    TagManager.create_tag("cuisine", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Cuisine", default_value={},
                          children=["asian","america","european","african"], render_priority=90)

    TagManager.create_tag("america", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="America", default_value=False,
                          children=["mexican"], render_priority=40)

    TagManager.create_tag("mexican", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Mexican", default_value=False,
                          children=[], render_priority=90)

    TagManager.create_tag("european", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="European", default_value=False,
                          children=[], render_priority=20)

    TagManager.create_tag("african", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="African", default_value=False,
                          children=[], render_priority=30)

    TagManager.create_tag("asian", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Asian", default_value=False,
                          children=["japanese", "indian","korean","tibetan","thai","western_asia","chinese"], render_priority=10)

    TagManager.create_tag("western_asia", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Western Asian", default_value=False,
                          children=[], render_priority=20)

    TagManager.create_tag("thai", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Thai", default_value=False,render_priority=50)

    TagManager.create_tag("chinese", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Chinese", default_value=False,render_priority=70)

    TagManager.create_tag("korean", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Korean", default_value=False,render_priority=60)

    TagManager.create_tag("tibetan", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Tibetan", default_value=False,render_priority=40)

    TagManager.create_tag("indian", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Indian", default_value=False
                          , render_priority=10)

    TagManager.create_tag("japanese", data_type=DataType.HIERARCHICAL_BOOL,
                          display_name="Japanese", default_value=False,
                          render_priority=30)




    # [Tag name, Column Name, Default value if tag is not set]...
    TagManager.set_search_columns(["name", "duration", "rating"])
    TagManager.auto_fill_void_tag_args()
    TagManager.create_parent_edges()
    TagManager.init_complete()
# TODO verschieden Cuise definieren e.g Indian, Japanase
