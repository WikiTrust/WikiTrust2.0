use parse_wiki_text::{DefinitionListItemType, Node, TableCellType};
use wasm_bindgen::prelude::*;
use web_sys::console;

pub fn set_panic_hook() {
    // When the `console_error_panic_hook` feature is enabled, we can call the
    // `set_panic_hook` function at least once during initialization, and then
    // we will get better error messages if our code ever panics.
    //
    // For more details see
    // https://github.com/rustwasm/console_error_panic_hook#readme
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}

pub fn log(s: &str) {
    console::log_1(&JsValue::from_str(s));
}

fn get_text_nodes(node_list: &Vec<Node>) -> String {
    let mut all_text: String = "".to_string();
    for node in node_list {
        match node {
            Node::Text {
                end: _,
                value,
                start: _,
            } => {
                all_text.push_str(value);
                // log(value)
            }
            Node::Heading {
                end: _,
                level,
                nodes,
                start,
            } => {
                // log("Heading");
                all_text.push_str(&get_text_nodes(nodes));
            }
            Node::CharacterEntity {
                character,
                end: _,
                start,
            } => {
                // log("Char Entity");
                // log(&character.to_string());
                all_text.push_str(&character.to_string());
            }
            Node::Link {
                end: _,
                start,
                target,
                text,
            } => {
                // log("Link");
                all_text.push_str(&get_text_nodes(text));
            }
            Node::ExternalLink {
                end: _,
                nodes,
                start: _,
            } => {
                // log("ExternalLink");
                all_text.push_str(&get_text_nodes(nodes));
            }
            Node::Preformatted {
                end: _,
                nodes,
                start: _,
            } => {
                // log("Preformatted");
                all_text.push_str(&get_text_nodes(nodes));
            }
            Node::UnorderedList {
                end: _,
                items,
                start: _,
            } => {
                // log("UnorderedList");
                for item in items {
                    all_text.push_str(&get_text_nodes(&item.nodes));
                }
            }
            Node::OrderedList {
                end: _,
                items,
                start: _,
            } => {
                // log("OrderedList");
                for item in items {
                    all_text.push_str(&get_text_nodes(&item.nodes));
                }
            }
            Node::DefinitionList {
                end: _,
                items,
                start: _,
            } => {
                // log("DefinitionList");
                for item in items {
                    all_text.push_str(&get_text_nodes(&item.nodes));
                }
            }
            Node::ParagraphBreak { end: _, start: _ } => {
                // log("ParagraphBreak");
                all_text.push_str("\n");
            }
            Node::HorizontalDivider { end: _, start: _ } => {
                // log("HorizontalDivider");
                all_text.push_str("\n");
            }
            _ => {
                // log("Un-handled Node");
            }
        }
    }
    return all_text;
}
pub fn parse(wiki_text: &str) -> String {
    let result = ::parse_wiki_text::Configuration::default().parse(&wiki_text);
    for warning in result.warnings {
        log(warning.message.message());
        let range: &str = &format!(
            "{} end: {}",
            (warning.start as u32).to_string(),
            (warning.end as u32).to_string()
        );
        log(range);
    }
    let all_text: String = get_text_nodes(&result.nodes);
    return all_text;
}
